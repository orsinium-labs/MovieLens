
class GlobalMeanEstimator:
    """Estimate every rating as global mean value

    This is dummiest algorithm. Every other realisation must be better.
    This is our floor estimator.
    """
    def fit(self, dataset):
        self._mean = dataset.df.rating.mean()

    def estimate(self, user: int, movie: int):
        return self._mean
