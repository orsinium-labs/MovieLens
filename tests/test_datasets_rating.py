# external
import numpy

# project
from movielens.datasets import RatingData


def test_users():
    ds = RatingData(full=False)
    users = ds.users
    assert 1 in users
    assert 2 in users
    assert numpy.where(users == 1) < numpy.where(users == 2)


def test_movies():
    ds = RatingData(full=False)
    movies = ds.movies
    assert 1 in movies
    assert 2 in movies
    assert numpy.where(movies == 1) < numpy.where(movies == 2)
