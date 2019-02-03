from .base import BaseSelector
from typing import List
import numpy
from tqdm import tqdm
from ..datasets import RatingData, MovieData
from collections import Counter


class GenreSelector(BaseSelector):
    """Return best movies in the genre
    """
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        self._movies_count = max(movies.movies) + 1
        self._ratings = numpy.zeros(self._movies_count)
        for movie in tqdm(movies.movies):
            self._ratings[movie] = ratings.df[ratings.df['movieId'] == movie].rating.mean()

        self._genres = dict()
        for genre in tqdm(movies.genres):
            self._genres[genre] = movies.get_genre(genre)
        self._movies = movies

    def select(self, movie: int) -> List[float]:
        counter = Counter()
        genres = self._movies.get_genres(movie)
        part = 1 / len(genres)
        for genre in genres:
            for movie2 in self._genres[genre]:
                counter[movie2] += part

        result = numpy.zeros(self._movies_count)
        for movie2, part in counter.items():
            result[movie2] = part * self._ratings[movie2]
        return result
