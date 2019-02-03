import ctypes

users_type = ctypes.c_int32 * 3
movies_type = ctypes.c_int32 * 3
ratings_type = ctypes.c_int32 * 3


class GoSlice(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_float)),
        ("len", ctypes.c_size_t),
    ]


lib = ctypes.cdll.LoadLibrary("./main.so")
lib.BuildSlopeOne.argtypes = [users_type, movies_type, ratings_type]
lib.BuildSlopeOne.restype = GoSlice


print(lib.BuildSlopeOne(
    users_type(1, 2, 3),
    movies_type(4, 5, 6),
    ratings_type(7, 8, 9),
))
