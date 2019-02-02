from typing import Optional
import numpy

from .base import BaseData


class RatingData(BaseData):
    _file_name = 'ratings.csv'

    @property
    def users(self) -> numpy.ndarray:
        return self.df['userId'].unique()

    @property
    def movies(self) -> numpy.ndarray:
        return numpy.sort(self.df['movieId'].unique())

    def get_rating(self, user: int, movie: int) -> Optional[int]:
        filtered = self.df[self.df['userId'] == user][self.df['movieId'] == movie]
        if filtered.empty():
            return None
        return next(iter(filtered['rating']))

    @property
    def matrix(self) -> numpy.ndarray:
        users = self.users
        movies = self.movies
        matrix = numpy.zeros((len(users), len(movies)))
        for _index, row in self.df.iterrows():
            user_index = numpy.where(users == row['userId'])
            movie_index = numpy.where(movies == row['movieId'])
            matrix[user_index][movie_index] = row['rating']
        return matrix
