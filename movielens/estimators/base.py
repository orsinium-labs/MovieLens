# built-in
import abc

# app
from ..datasets import MovieData, RatingData


class BaseEstimator(abc.ABC):
    @abc.abstractmethod
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        pass

    @abc.abstractmethod
    def estimate(self, user: int, movie: int) -> float:
        pass
