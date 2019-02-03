from movielens import recommend, estimators, RatingData, MovieData, preprocess


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
