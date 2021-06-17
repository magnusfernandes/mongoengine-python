from datetime import datetime, timedelta
import base64
import requests


class SpotifyAPI(object):
    tokenUrl = "https://accounts.spotify.com/api/token"
    accessToken = None
    tokenExpiry = datetime.now()
    clientId = None
    clientSecret = None
    tokenDidExpire = True

    def __init__(self, clientId, clientSecret):
        self.clientId = clientId
        self.clientSecret = clientSecret

    def getClientCreds(self):
        clientId = self.clientId
        clientSecret = self.clientSecret
        if clientId == None or clientSecret == None:
            raise Exception("Provide client ID and client secret.")
        clientCreds = f"{clientId}:{clientSecret}"
        clientCredsEncoded = clientCreds.encode()
        clientCredsB64 = base64.b64encode(clientCredsEncoded)
        return clientCredsB64.decode()

    def getTokenHeaders(self):
        clientCredsB64 = self.getClientCreds()
        return {
            "Authorization": f"Basic {clientCredsB64}"
        }

    def getTokenData(self):
        return {
            "grant_type": "client_credentials"
        }

    def performAuth(self):
        resp = requests.post(
            self.tokenUrl,
            data=self.getTokenData(),
            headers=self.getTokenHeaders()
        )
        if resp.status_code not in range(200, 299):
            return False
        now = datetime.now()
        respData = resp.json()
        expires = now + timedelta(seconds=respData['expires_in'])
        self.accessToken = respData['access_token']
        self.tokenExpiry = expires
        self.tokenDidExpire = expires < now
        return True

    def getAccessToken(self):
        token = self.accessToken
        expires = self.tokenExpiry
        now = datetime.now()
        if expires < now or token == None:
            self.performAuth()
            return self.getAccessToken()
        return token
