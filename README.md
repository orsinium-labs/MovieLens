# MovieLens

## Content

1. [Research of time and rating distribution](./data_mining_rating.ipynb)
1. [Research of genres and years](./data_mining_movie.ipynb)
1. [movielens/estimators](./movielens/estimators) -- realization of rating estimators on Python.
1. [movielens/slope_one](./movielens/slope_one) -- realization of Slope One estimator on Go.

## Results

```
name                       rmse  mae   fit     predict
GlobalMeanEstimator        2.31  1.86   0.00s  0.01s
GroupMeanEstimator         2.15  1.69  13.54s  0.01s
SlopeOneGoEstimator        1.71  1.30  43.88s  0.18s
SimilarUsersEstimator      2.08  1.61  84.18s  0.70s
```

## Run estimators comparing

```bash
python3.7 compare.py
```

## Get recommendations

For user:

```python
>>> from movielens import recommend, estimators, RatingData, MovieData, preprocess
>>> ratings = RatingData()
>>> movies = MovieData()
>>> preprocess(ratings=ratings, movies=movies)
>>> train, test = ratings.split(elements=100)
>>>
>>> estimator = estimators.GroupMeanEstimator()
>>> estimator.fit(ratings=train, movies=movies)
>>>
>>> recs = recommend.by_user(
...     user=0,
...     estimator=estimator,
...     movies=ratings.movies,
...     count=6,
... )
>>> recs
[48, 433, 666, 1646, 2327, 2745]
>>> for rec in recs:
...     print(movies.get_title(rec))
...
Lamerica (1994)
What Happened Was... (1994)
Supercop 2 (Project S) (Chao ji ji hua) (1993)
Dirty Work (1998)
World Is Not Enough, The (1999)
Blood Simple (1984)
```

First user loves old movies. Indeed :)
