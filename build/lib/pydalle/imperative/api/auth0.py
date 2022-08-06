"""
This module contains the implementations of calls to the Auth0 API.
"""
from typing import Optional, Dict

from pydalle.functional.api.flow.auth0 import get_access_token_flow
from pydalle.functional.api.request.auth0 import urlsafe_b64encode_string
from pydalle.imperative.outside.internet import session_flow, session_flow_async
from pydalle.imperative.outside.sysrand import secure_random_choice


def get_access_token_from_credentials(username: str, password: str, domain: str, client_id: str,
                                      audience: str, redirect_uri: str, scope: str, headers: Optional[Dict[str, str]] = None) -> str:
    return session_flow(get_access_token_flow, headers,
                        username=username, password=password, domain=domain,
                        client_id=client_id, audience=audience,
                        redirect_uri=redirect_uri, scope=scope,
                        code_verifier=_random_secure_string(),
                        initial_state=_random_secure_urlsafe_b64encoded_string(),
                        nonce=_random_secure_urlsafe_b64encoded_string())


async def get_access_token_from_credentials_async(username: str, password: str, domain: str, client_id: str,
                                 audience: str, redirect_uri: str, scope: str,
                                 headers: Optional[Dict[str, str]] = None) -> str:
    return await session_flow_async(get_access_token_flow, headers,
                                    username=username, password=password, domain=domain,
                                    client_id=client_id, audience=audience,
                                    redirect_uri=redirect_uri, scope=scope,
                                    code_verifier=_random_secure_string(),
                                    initial_state=_random_secure_urlsafe_b64encoded_string(),
                                    nonce=_random_secure_urlsafe_b64encoded_string())


def _random_secure_urlsafe_b64encoded_string() -> str:
    """
    https://auth0.com/docs/get-started/authentication-and-authorization-flow/call-your-api-using-the-authorization-code-flow-with-pkce#javascript-sample
    """
    return urlsafe_b64encode_string(_random_secure_string())


_RANDOM_CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_~."


def _random_secure_string() -> str:
    """
    This is how it was basically implemented in auth0-spa-js
    """
    return "".join(secure_random_choice(_RANDOM_CHARACTERS) for _ in range(43))
