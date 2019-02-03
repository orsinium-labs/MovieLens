from .estimators.base import BaseEstimator
from typing import List, Optional
from collections import Counter


def by_user(*, user: int, estimator: BaseEstimator, movies: List[int],
            count: Optional[int] = None) -> List[float]:
    ratings = Counter()
    for movie in movies:
        ratings[movie] = estimator.estimate(user=user, movie=movie)
    return [movie for movie, rating in ratings.most_common(count)]
