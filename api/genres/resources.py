from .models import Genres


class GenreResources():
    def DumpGenres():
        savedGenres = []

        for lp in range(10):
            genre = Genres(
                name="Genre {}".format(lp),
                profilePic="https://i.pravatar.cc/150?img=12"
            ).save()
            savedGenres.append(genre)
        return savedGenres
