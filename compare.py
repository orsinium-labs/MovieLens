from time import time
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
    train, test = ratings.split(elements=100)

    header = '{name:25}  {rmse}  {mae}   {fit}    {predict}'.format(
        name='name', rmse='rmse', mae='mae', fit='fit', predict='predict',
    )
    print(header)
    table = [header]

    for estimator in ESTIMATORS:
        # fit
        fit_time = time()
        estimator.fit(ratings=train, movies=movies)
        fit_time = time() - fit_time

        # predict
        predictions = []
        predict_time = time()
        for _index, row in test.df.iterrows():
            prediction = estimator.estimate(user=row['userId'], movie=row['movieId'])
            predictions.append(Prediction(
                user=row['userId'],
                movie=row['movieId'],
                predicted=prediction,
                real=row['rating'],
            ))
        predict_time = time() - predict_time

        # make table
        line = '{name:25}  {rmse:.2f}  {mae:.2f}  {fit:2.2f}s  {predict:2.2f}s'.format(
            name=type(estimator).__name__,
            rmse=rmse(predictions),
            mae=mae(predictions),
            fit=fit_time,
            predict=predict_time,
        )
        table.append(line)
        print(line)

    print('-' * 80)
    print('\n'.join(table))


if __name__ == '__main__':
    main()
