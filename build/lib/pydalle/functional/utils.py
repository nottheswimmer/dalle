"""
This module contains functional utilities used throughout the codebase.
"""

from typing import Optional
from urllib.parse import parse_qs, urlparse

from pydalle.functional.types import HttpResponse, JsonDict, FlowError


def get_query_param(url: str, param: str) -> str:
    return parse_qs(urlparse(url).query)[param][0]


def send_from(generator, fn):
    r = yield next(generator)
    while True:
        try:
            r = yield generator.send(r)
        except StopIteration as e:
            return fn(e.value)


def try_json(r: HttpResponse, status_code: Optional[int] = None) -> JsonDict:
    if status_code is not None and r.status_code != status_code:
        raise FlowError("Request returned an unexpected status code", r)
    try:
        out = r.json()
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e
    if not isinstance(out, dict):
        raise FlowError("Response was not a JSON object", r)
    return out


def filter_none(d: JsonDict) -> JsonDict:
    return {k: v for k, v in d.items() if v is not None}
