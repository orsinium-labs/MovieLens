from tqdm import tqdm
import numpy
from ..datasets import RatingData, MovieData


class GroupMeanEstimator:
    """Returns mean rating for movie genre and year.

    It's helpful when we know nothing about user.
    In the real world big companies also use item time in calculations
    to give priority to a new content.
    """

    def fit(self, ratings: RatingData, movies: MovieData) -> None:
        self._means = numpy.zeros(len(movies.movies))
        for _params, group in tqdm(movies.df.groupby(['genres', 'year'])):
            filtered_ratings = ratings.df[ratings.df['movieId'].isin(group['movieId'])]
            mean = filtered_ratings['rating'].mean()
            for movie in group['movieId']:
                self._means[int(movie)] = mean

    def estimate(self, user: int, movie: int) -> float:
        estimated = self._means[movie]
        if estimated == 0:
            return numpy.mean(self._means)
        return estimated
