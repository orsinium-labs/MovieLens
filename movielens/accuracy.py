from typing import List
from .prediction import Prediction
import numpy


def rmse(predictions: List[Prediction]) -> float:
    diffs = [prediction.diff ** 2 for prediction in predictions]
    return numpy.sqrt(numpy.mean(diffs))


def mae(predictions: List[Prediction]) -> float:
    diffs = [prediction.diff for prediction in predictions]
    return numpy.mean(diffs)
