# MovieLens

## Content

1. [Research of time and rating distribution](./data_mining_rating.ipynb)
1. [Research of genres and years](./data_mining_movie.ipynb)
1. [movielens/estimators](./movielens/estimators) -- realization of rating estimators on Python.
1. [movielens/slope_one](./movielens/slope_one) -- realization of Slope One estimator on Go.

## Estimators

Estimators predict rating for given user and movie. In other words it is predicted rating that given user can give to given movie.

1. **GlobalMeanEstimator** -- returns global mean rating by all movies. This is most dummy estimation. Every another smart estimator must be better.
1. **GroupMeanEstimator** -- returns mean rating for this genre and year. It's user independent estimation and can be used when we know nothing about user.
1. **MovieMeanEstimator** -- return mean rating for given movie. Also user independent estimation.
1. **SimilarUsersEstimator** -- estimate movie rating by weighted mean among similar users where weight is similarity of two users.
1. **SlopeOneGoEstimator** -- Go implementation of [Slope One](https://en.wikipedia.org/wiki/Slope_One) algortihm. I've made fit of this model on Go because Python implementation (**SlopeOneEstimator**) is much slower (2 hours against 20 seconds).

## Selectors

Selectors selects n most similar movies for given movie.

1. **GenreSelector** -- returns best movies in genres of given movie. Also position in rating depends on count of common genres.
1. **SimilarSelector** -- returns movies sorted by rating multiplied on genres and years similarity of movies to given movie.

## Results

```
name                       rmse  mae   fit     predict
GlobalMeanEstimator        1.95  1.54  00.00s  0.01s
SimilarUsersEstimator      1.85  1.44  40.08s  0.34s
MovieMeanEstimator         1.84  1.41  04.58s  0.01s
GroupMeanEstimator         1.74  1.34  06.48s  0.01s
SlopeOneGoEstimator        1.54  1.21  22.61s  0.09s
```

## Run estimators comparing

```bash
python3.7 compare.py
```

## Get recommendations

### For user

Get datasets:

```python
>>> from movielens import recommend, estimators, RatingData, MovieData, preprocess
>>> ratings = RatingData()
>>> movies = MovieData()
>>> preprocess(ratings=ratings, movies=movies)
>>> train, test = ratings.split(elements=100)
```

Train estimator:

```python
>>> estimator = estimators.GroupMeanEstimator()
>>> estimator.fit(ratings=train, movies=movies)
```

Get recommendations:

```python
>>> recs = recommend.by_user(
...     user=0,
...     estimator=estimator,
...     movies=ratings.movies,
...     count=6,
... )
>>> recs
[48, 433, 666, 1646, 2327, 2745]
```

Get movies titles:

```python
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

### For movie

Get datasets:

```python
>>> from movielens import recommend, selectors, RatingData, MovieData, preprocess
>>> ratings = RatingData()
>>> movies = MovieData()
>>> preprocess(ratings=ratings, movies=movies)
>>> train, test = ratings.split(elements=100)
```

Train estimator:

```python
>>> selector = selectors.GenreSelector()
>>> selector.fit(ratings=train, movies=movies)
```

Get recommendations:

```python
>>> recs = recommend.by_movie(
...     movie=0,  # Toy Story
...     selector=selector,
...     movies=ratings.movies,
...     count=6,
... )
>>> recs
[7742, 7338, 7787, 7899, 8656, 8689]
```

Get movies titles:

```python
>>> for rec in recs:
...     print(movies.get_title(rec))
...
Immortals (2011)
Blue Valentine (2010)
Iron Lady, The (2011)
Madagascar 3: Europe's Most Wanted (2012)
Patton Oswalt: My Weakness Is Strong (2009)
Ant-Man (2015)
