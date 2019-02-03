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
