"""
This module contains functions which are used to construct requests to the Auth0 API.
"""

import json
from base64 import urlsafe_b64encode
from hashlib import sha256
from urllib.parse import urlencode

from pydalle.functional.assumptions import AUTH0_TOKEN_URL_TEMPLATE, AUTH0_AUTHORIZE_URL_TEMPLATE
from pydalle.functional.types import HttpRequest


def request_access_token(client_id, code, code_verifier, domain, redirect_uri):
    return HttpRequest(**{
        "method": "post",
        "url": (AUTH0_TOKEN_URL_TEMPLATE % domain),
        "data": json.dumps({
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "code_verifier": code_verifier,
            "redirect_uri": redirect_uri,
        }),
        "headers": {"Content-Type": "application/json"},
    })


def request_provide_username_password(password_url, username, password, state, sleep=None):
    return HttpRequest(**{
        "method": "post",
        "url": password_url,
        "data": urlencode({
            "username": username,
            "password": password,
            "action": "default",
            "state": state,
        }),
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    }, sleep=sleep)


def request_provide_username(username_url, username, state):
    return HttpRequest(**{
        "method": "post",
        "url": username_url,
        "data": urlencode({
            "username": username,
            "action": "default",
            "state": state,
        }),
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    })


def request_authorization_code(audience, client_id, code_verifier, domain, initial_state, nonce, redirect_uri, scope):
    return HttpRequest(**{
        "method": "get",
        "url": (AUTH0_AUTHORIZE_URL_TEMPLATE % domain),
        "params": {
            "client_id": client_id,
            "audience": audience,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "response_type": "code",
            "response_mode": "query",
            "state": initial_state,
            "nonce": nonce,
            "code_challenge": _create_code_challenge(code_verifier),
            "code_challenge_method": "S256",
            "max_age": "0",
        }})


def urlsafe_b64encode_string(s: str) -> str:
    return _urlsafe_b64encode_hex_string(s.encode())


def _create_code_challenge(code_verifier: str) -> str:
    return _urlsafe_b64encode_hex_string(_sha256_string_hex(code_verifier))


def _urlsafe_b64encode_hex_string(s: bytes) -> str:
    return urlsafe_b64encode(s).rstrip(b"=").decode()


def _sha256_string_hex(s: str) -> bytes:
    return sha256(s.encode()).digest()
