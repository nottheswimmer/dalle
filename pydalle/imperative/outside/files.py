"""
This module contains all functions pydalle uses to interface with the filesystem.
"""

import warnings
from os import PathLike
from typing import Union, IO

try:
    import aiofiles
except ImportError as _e:
    from pydalle.functional.types import LazyImportError

    aiofiles = LazyImportError("aiofiles", _e)
    del LazyImportError


def read_bytes(file_like: Union[str, PathLike, IO[bytes]]) -> bytes:
    if isinstance(file_like, (str, PathLike)):
        with open(file_like, "rb") as f:
            return f.read()
    return file_like.read()


async def read_bytes_async(file_like: Union[str, PathLike, IO[bytes]]) -> bytes:
    if isinstance(file_like, (str, PathLike)):
        try:
            async with aiofiles.open(file_like, "rb") as f:
                return await f.read()
        except ImportError as _e:
            warnings.warn(f"aiofiles not found, falling back to sync version: {_e}", RuntimeWarning)
            return read_bytes(file_like)
    return file_like.read()
