from dalle.functional.assumptions import OPENAI_AUTH0_DOMAIN, OPENAI_AUTH0_CLIENT_ID, \
    OPENAI_AUTH0_AUDIENCE, OPENAI_LABS_REDIRECT_URI, OPENAI_AUTH0_SCOPE
from dalle.functional.api.flow.labs import get_bearer_token_flow
from dalle.imperative.api.auth0 import get_access_token, get_access_token_async
from dalle.imperative.outside.internet import session_flow, session_flow_async

_LABS_AUTH0_PARAMS = {
    "domain": OPENAI_AUTH0_DOMAIN,
    "client_id": OPENAI_AUTH0_CLIENT_ID,
    "audience": OPENAI_AUTH0_AUDIENCE,
    "redirect_uri": OPENAI_LABS_REDIRECT_URI,
    "scope": OPENAI_AUTH0_SCOPE,
}


def get_bearer_token(username: str, password: str) -> str:
    access_token = get_access_token(username, password, **_LABS_AUTH0_PARAMS)
    return session_flow(get_bearer_token_flow, access_token=access_token)


async def get_bearer_token_async(username: str, password: str) -> str:
    access_token = (await get_access_token_async(username, password, **_LABS_AUTH0_PARAMS))
    return await session_flow_async(get_bearer_token_flow, access_token=access_token)
