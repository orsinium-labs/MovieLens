# built-in
from collections import Counter
from typing import List, Optional

# app
from .estimators.base import BaseEstimator
from .selectors.base import BaseSelector


def by_user(*, user: int, estimator: BaseEstimator, movies: List[int],
            count: Optional[int] = None) -> List[int]:
    ratings = Counter()
    for movie in movies:
        ratings[movie] = estimator.estimate(user=user, movie=movie)
    return [movie for movie, rating in ratings.most_common(count)]


def by_movie(*, movie: int, selector: BaseSelector, movies: List[int],
             count: Optional[int] = None) -> List[int]:
    ratings = Counter(dict(
        enumerate(selector.select(movie=movie)),
    ))
    return [movie for movie, rating in ratings.most_common(count)]
