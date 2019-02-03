from math import isclose
from movielens.slope_one import build_slope_one


def test_build_slope_one():
    diffs = build_slope_one(
        users=[  0, 0, 0, 1, 1, 2, 2],  # noqa: E201
        movies=[ 0, 1, 2, 0, 1, 1, 2],  # noqa: E201
        ratings=[5, 3, 2, 3, 4, 2, 5],
    )
    assert isclose(diffs[0][1], .5)
