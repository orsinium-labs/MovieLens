# project
from movielens import MovieData, RatingData, estimators, preprocess, recommend, selectors


def test_by_user():
    ratings = RatingData()
    movies = MovieData()
    preprocess(ratings=ratings, movies=movies)
    train, test = ratings.split(elements=100)

    estimator = estimators.GroupMeanEstimator()
    estimator.fit(ratings=train, movies=movies)

    recs = recommend.by_user(
        user=0,
        estimator=estimator,
        movies=ratings.movies,
        count=6,
    )

    assert len(recs) == 6
    assert len(set(recs)) == 6


def test_by_movie():
    ratings = RatingData()
    movies = MovieData()
    preprocess(ratings=ratings, movies=movies)
    train, test = ratings.split(elements=100)

    selector = selectors.GenreSelector()
    selector.fit(ratings=train, movies=movies)

    recs = recommend.by_movie(
        movie=0,  # Toy Story
        selector=selector,
        movies=ratings.movies,
        count=6,
    )

    assert len(recs) == 6
    assert len(set(recs)) == 6
