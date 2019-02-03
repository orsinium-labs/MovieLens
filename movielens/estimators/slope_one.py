import numpy
from tqdm import tqdm
from ..datasets import RatingData, MovieData


class SlopeOneEstimator:
    """
    This realisation hasn't been tested because this is too slow.
    Instead of this I've made realisation on Go.
    It takes 40 seconds against 3 hours.

    https://en.wikipedia.org/wiki/Slope_One
    https://arxiv.org/pdf/cs/0702144.pdf
    https://github.com/NicolasHug/Surprise/blob/master/surprise/prediction_algorithms/slope_one.pyx
    """
    def fit(self, ratings: RatingData, movies: MovieData):
        movies_count = len(ratings.movies)
        counts = numpy.zeros((movies_count, movies_count), numpy.int)
        deviation = numpy.zeros((movies_count, movies_count), numpy.double)

        for user, group in tqdm(ratings.df.groupby('userId')):
            for _i, row1 in group.iterrows():
                for _i, row2 in group.iterrows():
                    counts[row1['movieId']][row2['movieId']] += 1
                    deviation[row1['movieId']][row2['movieId']] += row1['rating'] - row2['rating']

        for movie1 in tqdm(range(movies_count)):
            deviation[movie1][movie1] = 0  # I like to movie movie
            for movie2 in range(movie1 + 1, movies_count):
                deviation[movie1][movie2] /= counts[movie1][movie2]
                deviation[movie2][movie1] = -deviation[movie1][movie2]

        means = numpy.zeros((len(ratings.users),))
        for user, group in ratings.df.groupby('userId'):
            means[user] = group['rating'].mean()

        self._counts = counts
        self._deviation = deviation
        self._means = means
        self._dataset = ratings

    def estimate(self, user: int, movie: int) -> float:
        relevant = []
        for movie2 in self._dataset.get_movies(user=user):
            if self._counts[movie][movie2]:
                relevant.append(movie2)

        mean = self._means[user]
        if mean == 0:
            return numpy.mean(self._means)
        if not relevant:
            return mean

        deviation = sum(self._deviation[movie][movie2] for movie2 in relevant)
        return mean + deviation / len(relevant)
