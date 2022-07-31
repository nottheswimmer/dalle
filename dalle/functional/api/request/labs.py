from dalle.functional.assumptions import OPENAI_LABS_TASKS_URL, OPENAI_LABS_LOGIN_URL
from dalle.functional.types import HttpRequest


def check_task_request(from_ts) -> HttpRequest:
    return HttpRequest(method="get", url=OPENAI_LABS_TASKS_URL, params={"from_ts": from_ts})


def login_request(access_token) -> HttpRequest:
    return HttpRequest(method="post", url=OPENAI_LABS_LOGIN_URL, headers={"Authorization": f"Bearer {access_token}"})
