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


_CENSORED_REQUEST_KEYS = {"authorization", "password", "code", "code_verifier"}


@dataclass
class HttpResponse:
    status_code: int
    url: str
    text: str
    request: HttpRequest

    def json(self, **kwargs) -> 'JsonValue':
        return json.loads(self.text, **kwargs)

    def censor_request(self):
        """
        Try to censor sensitive data in the request if this may be printed as part of an error message or a traceback
        """
        self.request = deepcopy(self.request)  # Don't modify the original request
        # Censor parameters
        if self.request.params:
            for param in self.request.params:
                if param.lower() in _CENSORED_REQUEST_KEYS:
                    self.request.params[param] = "***REDACTED***"
        # Censor headers
        if self.request.headers:
            for header in self.request.headers:
                if header.lower() in _CENSORED_REQUEST_KEYS:
                    self.request.headers[header] = "***REDACTED***"
        # Censor data
        if self.request.data:
            try:
                # If it's JSON...
                data = json.loads(self.request.data)
                for key in data:
                    if key.lower() in _CENSORED_REQUEST_KEYS:
                        data[key] = "***REDACTED***"
                self.request.data = json.dumps(data)
            except json.JSONDecodeError:
                pass
            try:
                # If it's a query string...
                data = parse_qs(self.request.data)
                for key in data:
                    if key.lower() in _CENSORED_REQUEST_KEYS:
                        data[key] = ["***REDACTED***"]
                self.request.data = urlencode(data)
            except ValueError:
                pass


HttpFlow = Generator[HttpRequest, HttpResponse, T]
HttpFlowFunc = Callable[[Any], HttpFlow[T]]


class FlowError(Exception):
    def __init__(self, message: str, response: HttpResponse, *args: Any, censor: bool = True):
        if censor:
            response.censor_request()
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

    def throw(self):
        raise ImportError(f"""\
The {self.name} package is required for this module.
To install it, run:
    pip install {self.name}""") from self.e

    def __call__(self, *args, **kwargs):
        self.throw()

    def __getattr__(self, name):
        self.throw()
