from movielens import mae, rmse, RatingData, MovieData, preprocess, Prediction
from movielens.estimators import GlobalMeanEstimator

ESTIMATORS = (
    GlobalMeanEstimator(),
)


def main():
    ratings = RatingData()
    movies = MovieData()
    preprocess(ratings=ratings, movies=movies)
    train, test = ratings.split(elements=10)

    print('{name:25}   {rmse}   {mae}'.format(name='name', rmse='rmse', mae='mae'))

    for estimator in ESTIMATORS:
        estimator.fit(train)
        predictions = []
        for _index, row in test.df.iterrows():
            prediction = estimator.estimate(user=row['userId'], movie=row['movieId'])
            predictions.append(Prediction(
                user=row['userId'],
                movie=row['movieId'],
                predicted=prediction,
                real=row['rating'],
            ))
        print('{name:25}   {rmse:.2f}   {mae:.2f}'.format(
            name=type(estimator).__name__,
            rmse=rmse(predictions),
            mae=mae(predictions),
        ))


if __name__ == '__main__':
    main()
