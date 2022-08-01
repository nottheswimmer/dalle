from pydalle.functional.api.request.auth0 import request_access_token, request_provide_username_password, \
    request_provide_username, request_authorization_code
from pydalle.functional.types import HttpFlow, FlowError
from pydalle.functional.utils import get_query_param, send_from


def get_access_token_flow(*args, **kwargs) -> HttpFlow[str]:
    def fn(response):
        try:
            return response.json()["access_token"]
        except Exception as e:
            raise FlowError("Failed to get access token from response", response) from e

    return send_from(get_access_token_response_flow(*args, **kwargs), fn)


def get_access_token_response_flow(
        username: str,
        password: str,
        domain: str,
        client_id: str,
        audience: str,
        redirect_uri: str,
        scope: str,
        code_verifier: str,
        initial_state: str,
        nonce: str,
) -> HttpFlow[str]:
    """
    https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow
    """
    # Step 1: User -> Regular Web App: Click login link (No code necessary)
    # Step 2: Regular Web App -> Auth0 Tenant: Authorization Code Request to /authorize
    # Step 3: Auth0 Tenant -> User: Redirect to login/authorization prompt
    r = yield request_authorization_code(audience, client_id, code_verifier, domain, initial_state, nonce,
                                         redirect_uri, scope)
    if r.status_code != 200:
        raise FlowError("Failed to redirect to login/authorization prompt", r)
    # Step 4: User -> Auth0 Tenant: Authenticate and Consent
    try:
        state = get_query_param(r.url, "state")
    except Exception as e:
        raise FlowError("Failed to get state from redirect", r) from e
    r = yield request_provide_username(r.url, username, state)
    if r.status_code != 200:
        raise FlowError("Failed to provide username to auth0", r)
    # Step 4: User -> Auth0 Tenant: Authenticate and Consent (Continued)
    # Step 5: Auth0 Tenant -> Regular Web App: Authorization Code
    r = yield request_provide_username_password(r.url, username, password, state)
    if r.status_code != 200:
        raise FlowError("Failed to provide password to auth0", r)
    # Step 6. Auth0 Tenant -> Regular Web App: Authorization Code + Client ID + Client Secret to /oauth/token
    # Step 7. Auth0 Tenant: Validate Authorization Code + Client ID + Client Secret
    # Step 8. Auth0 Tenant -> Regular Web App: ID Token and Access Token
    try:
        code = get_query_param(r.url, "code")
    except Exception as e:
        raise FlowError("Failed to get code from redirect", r) from e
    r = yield request_access_token(client_id, code, code_verifier, domain, redirect_uri)
    if r.status_code != 200:
        raise FlowError("Failed to get access token", r)
    return r
