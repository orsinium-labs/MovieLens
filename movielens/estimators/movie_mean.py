# external
import numpy
from tqdm import tqdm

# app
from ..datasets import MovieData, RatingData
from .base import BaseEstimator


class MovieMeanEstimator(BaseEstimator):
    """Returns mean rating for given movie.
    """
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        mean = ratings.df.rating.mean()
        self._means = numpy.array([mean for _ in movies.movies])

        for movie in tqdm(movies.movies):
            mean = ratings.df[ratings.df['movieId'] == movie].rating.mean()
            if not numpy.isnan(mean):
                self._means[movie] = mean

    def estimate(self, user: int, movie: int) -> float:
        return self._means[movie]
