"""
This module contains all functions pydalle uses to make requests to the internet.
"""

import asyncio
import time
from typing import Optional, Dict

try:
    import requests
except ImportError as _e:
    from pydalle.functional.types import LazyImportError

    requests = LazyImportError("requests", _e)
    del LazyImportError

try:
    import aiohttp
except ImportError as _e:
    from pydalle.functional.types import LazyImportError

    aiohttp = LazyImportError("aiohttp", _e)
    del LazyImportError

from pydalle.functional.types import HttpFlowFunc, T, HttpRequest, HttpResponse


def session_flow(__flow: HttpFlowFunc[T], __headers=Optional[Dict[str, str]], /, **kwargs) -> T:
    handler = __flow(**kwargs)
    next_request = next(handler)
    session = requests.Session()
    if __headers:
        session.headers.update(__headers)
    while True:
        try:
            response = request(next_request, session=session)
            next_request = handler.send(response)
        except StopIteration as e:
            return e.value


def request(r: HttpRequest, /, session: Optional['requests.Session'] = None) -> HttpResponse:
    if session is None:
        session = requests.Session()
    if r.sleep is not None:
        time.sleep(r.sleep)
    response = session.request(r.method, r.url, params=r.params, data=r.data, headers=r.headers)
    return _requests_response_to_http_response(response, r)


async def session_flow_async(__flow: HttpFlowFunc[T], __headers=Optional[Dict[str, str]], /, **kwargs) -> T:
    handler = __flow(**kwargs)
    next_request = next(handler)
    async with aiohttp.ClientSession() as session:
        if __headers:
            session.headers.update(__headers)
        while True:
            try:
                response = await request_async(next_request, session=session)
                next_request = handler.send(response)
            except StopIteration as e:
                return e.value


async def request_async(r: HttpRequest, /, session: Optional['aiohttp.ClientSession'] = None) -> HttpResponse:
    if not session:
        session = aiohttp
    if r.sleep is not None:
        await asyncio.sleep(r.sleep)
    async with session.request(r.method, r.url, params=r.params, data=r.data, headers=r.headers) as response:
        return await _aiohttp_response_to_http_response(response, r)


def _requests_response_to_http_response(response: 'requests.Response', http_request: HttpRequest) -> HttpResponse:
    return HttpResponse(status_code=response.status_code,
                        content=response.text if http_request.decode else response.content,
                        url=response.url, request=http_request)


async def _aiohttp_response_to_http_response(response: 'aiohttp.ClientResponse',
                                             http_request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        status_code=response.status,
        content=(await response.text()) if http_request.decode else (await response.read()),
        url=str(response.url),
        request=http_request)
