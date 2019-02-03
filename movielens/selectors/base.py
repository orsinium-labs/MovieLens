import abc
from typing import List
from ..datasets import RatingData, MovieData


class BaseSelector(abc.ABC):
    @abc.abstractmethod
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        pass

    @abc.abstractmethod
    def select(self, movie: int) -> List[int]:
        pass
