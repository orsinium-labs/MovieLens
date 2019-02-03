# built-in
import re
from typing import List, Optional

# external
import pandas

# app
from .base import BaseData


REX_YEAR = re.compile(r'.+\((\d+)\)')


class MovieData(BaseData):
    _file_name = 'movies.csv'

    def __init__(self, df: Optional[pandas.DataFrame] = None, *, full: bool = False):
        super().__init__(df=df, full=full)
        self.df.set_index('movieId', inplace=True)
        self.df['year'] = self.df['title'].apply(self._get_year)

    @staticmethod
    def _get_year(title: str) -> Optional[int]:
        match = REX_YEAR.search(title)
        if match:
            return int(match.groups()[0])
        return None  # mypy requires it

    @property
    def movies(self) -> List[int]:
        # already unique and sorted
        if 'movieId' in self.df.columns:
            return list(map(int, self.df['movieId']))
        return list(map(int, self.df.index))

    @property
    def years(self) -> List[int]:
        return sorted(self.df['year'])

    @property
    def genres(self) -> List[str]:
        result = set()
        for line in self.df.genres:
            result.update(line.split('|'))
        return sorted(result)

    def get_title(self, movie_id: int) -> str:
        return self.df.loc[movie_id].title

    def get_year(self, movie_id: int) -> int:
        return self.df.loc[movie_id].year

    def get_genres(self, movie_id: int) -> List[str]:
        genres = self.df.loc[movie_id].genres
        if not genres:
            return []
        return genres.split('|')

    def get_genre(self, genre_name: str) -> List[int]:
        result = []
        for index, row in self.df.iterrows():
            if genre_name in row.genres.split('|'):
                if 'movieId' in self.df.columns:
                    result.append(int(row['movieId']))
                else:
                    result.append(int(index))
        return result

    def get_genres_df(self) -> pandas.DataFrame:
        genres = list()
        for movie, row in self.df.iterrows():
            for genre in self.get_genres(movie):
                genres.append((genre, movie, row.year))
        genres = pandas.DataFrame(genres, columns=['genre', 'movie', 'year'])
        return genres
