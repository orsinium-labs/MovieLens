"""Select most similar movies for given movie.
"""
# app
from .genre import GenreSelector
from .similar import SimilarSelector


__all__ = [
    'GenreSelector',
    'SimilarSelector',
]
