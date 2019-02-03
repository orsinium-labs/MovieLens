import ctypes
from math import sqrt
from typing import List
import numpy


users_type = ctypes.c_int32 * 3
movies_type = ctypes.c_int32 * 3
ratings_type = ctypes.c_int32 * 3


# https://medium.com/learning-the-go-programming-language/calling-go-functions-from-other-languages-4c7d8bcc69bf
class GoSlice(ctypes.Structure):
    _fields_ = [
        ("len", ctypes.c_size_t),
        ("data", ctypes.POINTER(ctypes.c_float)),
    ]


lib = ctypes.cdll.LoadLibrary("./main.so")
lib.BuildSlopeOne.argtypes = [users_type, movies_type, ratings_type]
lib.BuildSlopeOne.restype = GoSlice


def build_slope_one(users: List[int], movies: List[int], ratings: List[int]) -> numpy.ndarray:
    result = lib.BuildSlopeOne(
        users_type(*users),
        movies_type(*movies),
        ratings_type(*ratings),
    )
    width = int(sqrt(result.len))
    array = numpy.array(result.data[:result.len])
    return array.reshape((width, width))


if __name__ == '__main__':
    print(build_slope_one([1, 2, 3], [4, 5, 6], [7, 8, 9]))
