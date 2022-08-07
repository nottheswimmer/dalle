"""
This module contains both type hints and structures used throughout the codebase.
"""

import json
from copy import deepcopy
from dataclasses import dataclass
from typing import TypeVar, Protocol, Optional, Dict, Generator, Callable, Any, Union, List
from urllib.parse import urlencode, parse_qs

T = TypeVar("T")
_T_co = TypeVar("_T_co", covariant=True)


class SupportsLenAndGetItem(Protocol[_T_co]):
    def __len__(self) -> int: ...

    def __getitem__(self, __k: int) -> _T_co: ...


@dataclass
class HttpRequest:
    method: str
    url: str
    params: Optional[Dict[str, Union[int, str]]] = None
    headers: Optional[Dict[str, str]] = None
    data: Optional[str] = None
    sleep: Optional[float] = None
    decode: bool = True


_CENSORED_REQUEST_KEYS = {"authorization", "password", "code", "code_verifier"}


@dataclass
class HttpResponse:
    status_code: int
    url: str
    content: Union[str, bytes]
    request: HttpRequest

    def json(self, **kwargs) -> 'JsonValue':
        return json.loads(self.content, **kwargs)

    def _to_censored_response(self) -> 'HttpResponse':
        """
        Try to censor sensitive data in the request if this may be printed as part of an error message or a traceback
        """
        new = deepcopy(self)
        # Censor parameters
        if new.request.params:
            for param in new.request.params:
                if param.lower() in _CENSORED_REQUEST_KEYS:
                    new.request.params[param] = "***REDACTED***"
        # Censor headers
        if new.request.headers:
            for header in new.request.headers:
                if header.lower() in _CENSORED_REQUEST_KEYS:
                    new.request.headers[header] = "***REDACTED***"
        # Censor data
        if new.request.data:
            try:
                # If it's JSON...
                data = json.loads(new.request.data)
                for key in data:
                    if key.lower() in _CENSORED_REQUEST_KEYS:
                        data[key] = "***REDACTED***"
                new.request.data = json.dumps(data)
            except json.JSONDecodeError:
                pass
            try:
                # If it's a query string...
                data = parse_qs(new.request.data)
                for key in data:
                    if key.lower() in _CENSORED_REQUEST_KEYS:
                        data[key] = ["***REDACTED***"]
                new.request.data = urlencode(data)
            except ValueError:
                pass
        return new


HttpFlow = Generator[HttpRequest, HttpResponse, T]
HttpFlowFunc = Callable[[Any], HttpFlow[T]]


class FlowError(Exception):
    def __init__(self, message: str, response: HttpResponse, *args: Any, censor: bool = True):
        if censor:
            response = response._to_censored_response()
        super().__init__(message, response, *args)
        self.response = response


# TODO: Recursive type hints. My IDE wasn't appreciating them for now.
# JsonValue = Union[str, int, float, bool, None, 'JsonDict', 'JsonList']
JsonValue = Any
JsonDict = Dict[str, JsonValue]
JsonList = List[JsonValue]


class LazyImportError:
    def __init__(self, name: str, e: ImportError):
        self.name = name
        self.e = e

    def throw(self, reason, *args, **kwargs):
        if reason == "__call__":
            prefix = f"{self.name}("
            prefix += ", ".join(map(str, args))
            prefix += ", " if args else ""
            prefix += ", ".join(f"{k}={v}" for k, v in kwargs.items())
            prefix += ")"
        elif reason == "__getattr__":
            prefix = f"{self.name}.{args[0]}"
        else:
            prefix = f"{self.name}.{reason}"

        raise ImportError(f"""\
{prefix}: The {self.name} package is required for this module.
To install it, run:
    pip install {self.name}""") from self.e

    def __call__(self, *args, **kwargs):
        self.throw("__call__", *args, **kwargs)

    def __getattr__(self, name):
        # Help readthedocs put something here for optional dependencies
        if name == "__qualname__":
            return self.name
        if name == "__args__":
            return ()
        self.throw("__getattr__", name)
