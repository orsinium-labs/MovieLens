"""Select most similar movies for given movie.
"""
from .genre import GenreSelector
from .similar import SimilarSelector

__all__ = [
    'GenreSelector',
    'SimilarSelector',
]
