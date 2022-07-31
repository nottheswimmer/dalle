from dalle.functional.api.request.labs import login_request
from dalle.functional.types import HttpFlow, FlowError, HttpResponse
from dalle.functional.utils import send_from


def get_bearer_token_response_flow(access_token: str) -> HttpFlow[HttpResponse]:
    r = yield login_request(access_token)
    if r.status_code != 200:
        raise FlowError("Failed to login", r)
    return r


def get_bearer_token_flow(access_token: str) -> HttpFlow[str]:
    def fn(response):
        try:
            return response.json()["user"]["session"]["sensitive_id"]
        except Exception as e:
            raise FlowError("Failed to get bearer token from response", response) from e

    return send_from(get_bearer_token_response_flow(access_token), fn)
