from pathlib import Path
import ctypes
from math import sqrt
from typing import List
import numpy


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
    result = lib.BuildSlopeOne(
        make_input(users, size),
        make_input(movies, size),
        make_input(ratings, size),
    )
    width = int(sqrt(result.len))
    array = numpy.array(result.data[:result.len])
    return array.reshape((width, width))


if __name__ == '__main__':
    print(build_slope_one([1, 2, 3], [4, 5, 6], [7, 8, 9]))
