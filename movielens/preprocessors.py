import numpy
from .datasets import RatingData, MovieData


def preprocess(ratings: RatingData, movies: MovieData) -> None:
    movies.df.reset_index(inplace=True)
    # make ids sequential
    for field, vector in [('movieId', ratings.movies), ('userId', ratings.users)]:
        for df in (ratings.df, movies.df):
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda source_id: numpy.where(vector == source_id),
                )

    # fill missed values
    movies.df['year'].fillna(method='bfill', inplace=True)
    movies.df['genres'] = movies.df['genres'].apply(lambda genres: '' if '(' in genres else genres)
