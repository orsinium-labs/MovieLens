import abc
from ..datasets import RatingData, MovieData


class BaseEstimator(abc.ABC):
    @abc.abstractmethod
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        pass

    @abc.abstractmethod
    def estimate(self, user: int, movie: int) -> float:
        return self._mean
