# built-in
import abc
from typing import List

# app
from ..datasets import MovieData, RatingData


class BaseSelector(abc.ABC):
    @abc.abstractmethod
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        pass

    @abc.abstractmethod
    def select(self, movie: int) -> List[int]:
        pass
