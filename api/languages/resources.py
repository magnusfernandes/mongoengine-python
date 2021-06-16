from .models import Languages


class LanguageResources():
    def DumpLanguages():
        savedLanguages = []

        for lp in range(10):
            language = Languages(
                name="Language {}".format(lp),
            ).save()
            savedLanguages.append(language)
        return savedLanguages
