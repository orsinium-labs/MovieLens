from pathlib import Path
import requests
from tqdm import tqdm_notebook
from zipfile import ZipFile
from typing import Optional
import pandas
import numpy
from shutil import rmtree


URL_SMALL = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
URL_FULL = 'http://files.grouplens.org/datasets/movielens/ml-20m.zip'


def download_data(*, full=False):
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


class RatingData:
    def __init__(self, df=None, *, full=False):
        if df is None:
            download_data(full=full)
            path = Path('data') / 'ratings.csv'
            df = pandas.read_csv(str(path))
            df['rating'] = df['rating'].apply(lambda rating: int(rating * 2))
        self.df = df

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
