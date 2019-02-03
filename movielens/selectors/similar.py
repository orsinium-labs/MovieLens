# built-in
from typing import List

# external
import numpy
from tqdm import tqdm

# app
from ..datasets import MovieData, RatingData
from .base import BaseSelector


class SimilarSelector(BaseSelector):
    """Return best movies from similar.

    I'm not sure about algorithm. This is from my sick head.
    I just get movie mean rating and multiply it on year diff (from 0 to 1)
    and common genres count from total genres into 2 movies (from 0 to 1).
    """
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        movies_count = len(movies.movies)
        movies_ratings = numpy.zeros(movies_count)
        for movie in tqdm(movies.movies):
            movies_ratings[movie] = ratings.df[ratings.df['movieId'] == movie].rating.mean()

        years_diff = max(movies.years) - min(movies.years) + 1
        self._similarity = numpy.zeros((movies_count, movies_count))

        genres_vector = {row['movieId']: set(row['genres'].split('|')) for _index, row in movies.df.iterrows()}
        years_vector = numpy.array([row['year'] for _index, row in movies.df.iterrows()], dtype=numpy.int16)

        for movie1 in tqdm(range(movies_count)):
            genres1 = genres_vector[movie1]
            year1 = years_vector[movie1]

            for movie2 in range(movies_count):
                genres2 = genres_vector[movie2]
                rating = movies_ratings[movie2]
                year_sim = 1 - numpy.abs(year1 - years_vector[movie2]) / years_diff
                genres_sim = len(genres1 & genres2) / len(genres1 | genres2)
                self._similarity[movie1][movie2] = rating * year_sim * genres_sim

    def select(self, movie: int) -> List[float]:
        return self._similarity[movie]
