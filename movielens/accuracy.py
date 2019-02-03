# built-in
from typing import List

# external
import numpy

# app
from .prediction import Prediction


def rmse(predictions: List[Prediction]) -> float:
    diffs = [prediction.diff ** 2 for prediction in predictions]
    return numpy.sqrt(numpy.mean(diffs))


def mae(predictions: List[Prediction]) -> float:
    diffs = [prediction.diff for prediction in predictions]
    return numpy.mean(diffs)
