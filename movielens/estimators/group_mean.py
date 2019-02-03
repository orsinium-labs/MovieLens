# external
import numpy
from tqdm import tqdm

# app
from ..datasets import MovieData, RatingData
from .base import BaseEstimator


class GroupMeanEstimator(BaseEstimator):
    """Returns mean rating for movie genre and year.

    It's helpful when we know nothing about user.
    In the real world big companies also use item time in calculations
    to give priority to a new content.
    """

    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        self._mean = ratings.df.rating.mean()

        self._means = numpy.array([self._mean for _ in movies.movies])
        for _params, group in tqdm(movies.df.groupby(['genres', 'year'])):
            filtered_ratings = ratings.df[ratings.df['movieId'].isin(group['movieId'])]
            mean = filtered_ratings['rating'].mean()
            if not numpy.isnan(mean):
                for movie in group['movieId']:
                    self._means[int(movie)] = mean

    def estimate(self, user: int, movie: int) -> float:
        return self._means[movie]
