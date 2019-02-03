from movielens import mae, rmse, RatingData, MovieData, preprocess, Prediction, estimators

ESTIMATORS = (
    estimators.GlobalMeanEstimator(),
    estimators.GroupMeanEstimator(),
    # estimators.SlopeOneEstimator(),
    estimators.SlopeOneGoEstimator(),
)


def main():
    ratings = RatingData()
    movies = MovieData()
    preprocess(ratings=ratings, movies=movies)
    train, test = ratings.split(elements=30)

    print('{name:25}   {rmse}   {mae}'.format(name='name', rmse='rmse', mae='mae'))
    table = []

    for estimator in ESTIMATORS:
        estimator.fit(ratings=train, movies=movies)
        predictions = []
        for _index, row in test.df.iterrows():
            prediction = estimator.estimate(user=row['userId'], movie=row['movieId'])
            predictions.append(Prediction(
                user=row['userId'],
                movie=row['movieId'],
                predicted=prediction,
                real=row['rating'],
            ))
        line = '{name:25}   {rmse:.2f}   {mae:.2f}'.format(
            name=type(estimator).__name__,
            rmse=rmse(predictions),
            mae=mae(predictions),
        )
        table.append(line)
        print(line)

    print('-' * 80)
    print('\n'.join(table))


if __name__ == '__main__':
    main()
