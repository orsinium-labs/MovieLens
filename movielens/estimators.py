

class FilmMeanAll:
    """estimate film rating for user by mean value of overall film rating
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmMeanSimilar:
    """estimate film rating for user by mean value of film rating among similar users.
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmGenreUser:
    """estimate film rating for user by genre that user likes
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmGenreSimilar:
    """estimate film rating for user by genre that similar users likes
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmYearUser:
    """estimate film rating for user by years that user likes
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmYearSimilar:
    """estimate film rating for user by years that similar users likes
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmSVD:
    """Make clusters by SVD algorithm
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...


class FilmBellKor:
    """estimate film rating by BellKor algorithm (Netflix Prize winners)

    https://github.com/FunctorML/BellkorAlgorithm
    """
    def fit(self, matrix):
        ...

    def estimate(self, vector):
        ...
