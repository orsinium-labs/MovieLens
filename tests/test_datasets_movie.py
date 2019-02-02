from movielens.datasets import MovieData
import numpy


def test_movies():
    ds = MovieData(full=False)
    movies = ds.movies
    assert 1 in movies
    assert 2 in movies
    assert numpy.where(movies == 1) < numpy.where(movies == 2)


def test_genres():
    ds = MovieData(full=False)
    genres = ds.genres
    assert 'Children' in genres
    assert 'Romance' in genres
    assert genres == sorted(genres)


def test_year():
    ds = MovieData(full=False)
    assert ds.get_year(2) == 1995
    assert ds.get_year(84246) == 1947


def test_title():
    ds = MovieData(full=False)
    assert ds.get_title(2) == 'Jumanji (1995)'
    assert ds.get_title(84246) == 'It Happened on Fifth Avenue (1947)'
