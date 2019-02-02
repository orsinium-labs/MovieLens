from pathlib import Path
import requests
from tqdm import tqdm_notebook
from zipfile import ZipFile
from typing import Optional, List
import pandas
import numpy
import re
from shutil import rmtree


REX_YEAR = re.compile(r'.+\((\d+)\)')
URL_SMALL = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
URL_FULL = 'http://files.grouplens.org/datasets/movielens/ml-20m.zip'


class BaseData:
    def __init__(self, df: Optional[pandas.DataFrame] = None, *, full: bool = False):
        if df is None:
            self.download_data(full=full)
            path = Path('data') / self._file_name
            df = pandas.read_csv(str(path))
            if 'rating' in df.columns:
                df['rating'] = df['rating'].apply(lambda rating: int(rating * 2))
        self.df = df

    @staticmethod
    def download_data(*, full: bool = False) -> None:
        if not Path('data').exists():
            # download archive
            if not Path('data.zip').exists():
                url = URL_FULL if full else URL_SMALL
                response = requests.get(url, stream=True)
                with Path('data.zip').open('wb') as stream:
                    size = int(response.headers.get('content-length')) / 1024 + 1
                    for chunk in tqdm_notebook(response.iter_content(chunk_size=1024), total=size):
                        if chunk:
                            stream.write(chunk)

            # extract archive
            with ZipFile('data.zip', 'r') as archive:
                archive.extractall('data')
            Path('data.zip').unlink()

            # mv files from nested dir
            for path in Path('data').glob('*/*.csv'):
                path.rename(Path('data') / path.name)

            # drop empty dir
            for path in Path('data').iterdir():
                if path.is_dir():
                    rmtree(str(path))


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
    def movies(self) -> numpy.ndarray:
        # already unique and sorted
        return self.df.index

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
                result.append(index)
        return result

    def get_genres_df(self) -> pandas.DataFrame:
        genres = list()
        for movie, row in self.df.iterrows():
            for genre in self.get_genres(movie):
                genres.append((genre, movie, row.year))
        genres = pandas.DataFrame(genres, columns=['genre', 'movie', 'year'])
        return genres
