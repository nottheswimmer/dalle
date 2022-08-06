"""
This module contains all functions pydalle uses which depend on the system's random number generator.
"""

import secrets

from pydalle.functional.types import SupportsLenAndGetItem, T


def secure_random_choice(seq: SupportsLenAndGetItem[T]) -> T:
    """
    Return a cryptographically secure random element from a sequence.
    """
    return secrets.choice(seq)
