from pathlib import Path
import requests
from tqdm import tqdm_notebook
from zipfile import ZipFile
from typing import Optional, Tuple
import pandas
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

    def split(self, elements: Optional[int] = None,
              ratio: Optional[float] = None) -> Tuple['BaseData', 'BaseData']:
        if elements is None:
            elements = int(len(self.df) * ratio)
        test = self.df.sample(elements)
        train = self.df.drop(index=test.index)
        cls = type(self)
        return cls(df=train), cls(df=test)
