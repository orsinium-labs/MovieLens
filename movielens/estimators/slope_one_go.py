import numpy
from ..datasets import RatingData, MovieData
from ..slope_one import build_slope_one
from .base import BaseEstimator


class SlopeOneGoEstimator(BaseEstimator):
    """
    https://github.com/ginuerzh/go-slope-one/blob/master/slope_one.go
    """
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        self._diffs = build_slope_one(
            users=ratings.df['userId'],
            movies=ratings.df['movieId'],
            ratings=ratings.df['rating'],
        )

        means = numpy.zeros((len(ratings.users),))
        for user, group in ratings.df.groupby('userId'):
            means[user] = group['rating'].mean()
        self._means = means
        self._dataset = ratings

    def estimate(self, user: int, movie: int) -> float:
        relevant = []
        for movie2 in self._dataset.get_movies(user=user):
            diff = self._diffs[movie][movie2]
            if diff > -15:
                relevant.append(diff)

        mean = self._means[user]
        if mean == 0:
            return numpy.mean(self._means)
        if not relevant:
            return mean

        return mean + numpy.mean(relevant)
