from functools import partial
import numpy
from typing import Optional
from .datasets import RatingData, MovieData


def _get_index(field, vector, source_id) -> Optional[int]:
    if field == 'userId':
        return source_id - 1
    places = numpy.where(vector == source_id)
    while not isinstance(places, (numpy.int64, int)):
        if len(places) == 0:
            return None
        places = places[0]
    return places


def preprocess(ratings: RatingData, movies: MovieData) -> None:
    movies.df.reset_index(inplace=True)
    # make ids sequential
    for field, vector in [('movieId', ratings.movies), ('userId', ratings.users)]:
        for df in (ratings.df, movies.df):
            if field in df.columns:
                df[field] = df[field].apply(partial(_get_index, field, vector))

    # fill missed values
    movies.df['year'].fillna(method='bfill', inplace=True)
    movies.df['genres'] = movies.df['genres'].apply(lambda genres: '' if '(' in genres else genres)

    # drop movies that has no rating (they can't get new id)
    movies.df.dropna(subset=['movieId'], inplace=True)
