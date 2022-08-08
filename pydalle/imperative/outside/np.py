"""
This module contains all functions pydalle uses to directly interface with numpy.
"""

try:
    from numpy import array, ndarray
except ImportError as e:
    from pydalle.functional.types import LazyImportError

    array = LazyImportError("numpy.array", e)
    ndarray = LazyImportError("numpy.ndarray", e)
    del LazyImportError

from pydalle.imperative.outside.pil import PILImageType, PILImage


def pil_image_to_np_array(image: PILImageType) -> 'ndarray':
    return array(image)


def np_array_to_pil_image(array: 'ndarray') -> PILImageType:
    return PILImage.fromarray(array)
