from typing import Optional

from dalle.functional.api.request.labs import login_request, get_tasks_request, create_task_request, get_task_request
from dalle.functional.api.response.labs import TaskList, TaskType, Task
from dalle.functional.types import HttpFlow, FlowError, JsonDict
from dalle.functional.utils import send_from, try_json

DEFAULT_INTERVAL = 1.0


def get_bearer_token_json_flow(access_token: str) -> HttpFlow[JsonDict]:
    r = yield login_request(access_token)
    while r.status_code == 504:
        r = yield login_request(access_token, sleep=DEFAULT_INTERVAL)
    return try_json(r, status_code=200)


def get_bearer_token_flow(access_token: str) -> HttpFlow[str]:
    def fn(response):
        try:
            return response["user"]["session"]["sensitive_id"]
        except Exception as e:
            raise FlowError("Failed to get bearer token from response", response) from e

    return send_from(get_bearer_token_json_flow(access_token), fn)


def get_tasks_flow(bearer_token: str, from_ts: Optional[int] = None) -> HttpFlow[TaskList]:
    r = yield get_tasks_request(bearer_token, from_ts)
    while r.status_code == 504:
        r = yield get_tasks_request(bearer_token, from_ts, sleep=DEFAULT_INTERVAL)
    j = try_json(r, status_code=200)
    try:
        return TaskList.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def create_task_flow(bearer_token: str,
                     caption: str,
                     task_type: TaskType = "text2im",
                     batch_size: int = 4) -> HttpFlow[Task]:
    r = yield create_task_request(bearer_token, caption, task_type, batch_size)
    while r.status_code == 504:
        r = yield create_task_request(bearer_token, caption, task_type, batch_size, sleep=DEFAULT_INTERVAL)
    j = try_json(r, status_code=200)
    try:
        return Task.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def create_text2im_task_flow(bearer_token: str, caption: str, batch_size: Optional[int] = 4) -> HttpFlow[Task]:
    return create_task_flow(bearer_token, caption=caption, task_type="text2im", batch_size=batch_size)


def get_task_flow(bearer_token: str, task_id: str) -> HttpFlow[Task]:
    r = yield get_task_request(bearer_token, task_id=task_id)
    while r.status_code == 504:
        r = yield get_task_request(bearer_token, task_id=task_id, sleep=DEFAULT_INTERVAL)
    j = try_json(r, status_code=200)
    try:
        return Task.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def poll_for_task_completion_flow(bearer_token: str,
                                  task_id: str,
                                  interval: float = DEFAULT_INTERVAL, _max_attempts: int = 1000) -> HttpFlow[Task]:
    r = yield get_task_request(bearer_token, task_id=task_id)
    for _ in range(_max_attempts):
        if r.status_code != 504:
            j = try_json(r, status_code=200)
            if j["status"] != "pending":
                try:
                    return Task.from_dict(j)
                except Exception as e:
                    raise FlowError("Failed to parse response", r) from e
        r = yield get_task_request(bearer_token, task_id=task_id, sleep=interval)
    raise FlowError("Failed to poll for task completion: Reached max attempts", r)
