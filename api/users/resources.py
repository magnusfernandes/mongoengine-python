from .models import Users


class UserResources():
    def DumpUsers():
        savedUsers = []

        for lp in range(10):
            user = Users(
                name="User {}".format(lp),
                email="user{}@gmail.com".format(lp)
            ).save()
            savedUsers.append(user)
        return savedUsers
