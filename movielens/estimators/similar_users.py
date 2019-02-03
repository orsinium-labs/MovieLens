import numpy
from tqdm import tqdm
from ..datasets import RatingData, MovieData
from collections import Counter
from math import isclose
from .base import BaseEstimator


class SimilarUsersEstimator(BaseEstimator):
    """Returns mean movie rating among similar users.

    It's weighted mean of movie ratings where weight is similarity of two users.
    """
    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        counters = dict()
        for user, group in ratings.df.groupby('userId'):
            group = group[['movieId', 'rating']]
            counters[user] = Counter(dict(group.itertuples(index=False)))

        users_count = len(counters)
        self._similarity = numpy.zeros((users_count, users_count))
        for user1, c1 in tqdm(counters.items()):
            for user2, c2 in counters.items():
                if user1 == user2:
                    self._similarity[user1][user2] = 1
                    continue

                common_movies = len(set(c1) & set(c2)) / len(c1)
                if isclose(common_movies, 0):
                    self._similarity[user1][user2] = 0
                    continue

                deviations = numpy.abs(list((c1 - c2).values()))
                rmse = numpy.sqrt(numpy.mean(deviations ** 2))
                self._similarity[user1][user2] = rmse * common_movies

        self._df = ratings.df

    def estimate(self, user: int, movie: int) -> float:
        rates = []
        weights = []
        for _index, row in self._df[self._df['movieId'] == movie].iterrows():
            sim = self._similarity[user][row['userId']]
            if isclose(sim, 0):
                continue
            rates.append(sim * row['rating'])
            weights.append(sim)

        # weighted mean by similar
        if weights:
            return numpy.sum(rates) / numpy.sum(weights)

        # mean by all for this movie
        mean = self._df[self._df['movieId'] == movie]['rating'].mean()
        if not numpy.isnan(mean):
            return mean

        # nobody rated this movie? Lol, ok, let's hjust return global mean
        return self._df['rating'].mean()
