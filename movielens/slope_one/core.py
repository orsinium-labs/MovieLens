# built-in
import ctypes
from logging import getLogger
from math import sqrt
from pathlib import Path
from typing import List

# external
import numpy


logger = getLogger(__name__)


class GoSliceOutput(ctypes.Structure):
    _fields_ = [
        ("len", ctypes.c_size_t),
        ("data", ctypes.POINTER(ctypes.c_float)),
    ]


# https://medium.com/learning-the-go-programming-language/calling-go-functions-from-other-languages-4c7d8bcc69bf
class GoSliceInput(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_void_p)),
        ("len", ctypes.c_longlong),
        ("cap", ctypes.c_longlong),
    ]


def make_input(data, size):
    return GoSliceInput((ctypes.c_void_p * size)(*data), size, size)


path = Path(__file__).resolve().parent
lib = ctypes.cdll.LoadLibrary(str(path / 'main.so'))
lib.BuildSlopeOne.argtypes = [GoSliceInput, GoSliceInput, GoSliceInput]
lib.BuildSlopeOne.restype = GoSliceOutput


def build_slope_one(users: List[int], movies: List[int], ratings: List[int]) -> numpy.ndarray:
    size = len(users)
    logger.debug('start go call')
    result = lib.BuildSlopeOne(
        make_input(users, size),
        make_input(movies, size),
        make_input(ratings, size),
    )
    logger.debug('end go call')
    width = int(sqrt(result.len))
    array = numpy.zeros(result.len)
    for i in range(result.len):
        array[i] = result.data[i]
    logger.debug('numpy array is ready')
    return array.reshape((width, width))


if __name__ == '__main__':
    print(build_slope_one([1, 2, 3], [4, 5, 6], [7, 8, 9]))
