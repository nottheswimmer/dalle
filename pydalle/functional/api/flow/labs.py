"""
This module contains functions which are used handle the flow of requests to the labs API.
"""

from typing import Optional, List

from pydalle.functional.api.request.labs import login_request, get_tasks_request, create_task_request, \
    get_task_request, download_generation_request, save_generations_request, share_generation_request, \
    flag_generation_request, get_credit_summary_request, get_generation_request
from pydalle.functional.api.response.labs import TaskList, TaskType, Task, Generation, Collection, Login, UserFlag, \
    BillingInfo
from pydalle.functional.types import HttpFlow, FlowError, JsonDict
from pydalle.functional.utils import send_from, try_json

DEFAULT_INTERVAL = 1.0


def get_login_info_json_flow(access_token: str) -> HttpFlow[JsonDict]:
    if access_token.startswith("sess-"):
        raise ValueError("Invalid access token: It appears you've passed in a session "
                        "token instead of the expected access token")
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

    return send_from(get_login_info_json_flow(access_token), fn)


def get_login_info_flow(access_token: str) -> HttpFlow[Login]:
    def fn(response):
        try:
            return Login.from_dict(response)
        except Exception as e:
            raise FlowError("Failed to parse response", response) from e

    return send_from(get_login_info_json_flow(access_token), fn)



def get_tasks_flow(bearer_token: str, limit: Optional[int] = None, from_ts: Optional[int] = None) -> HttpFlow[TaskList]:
    r = yield get_tasks_request(bearer_token, limit, from_ts)
    while r.status_code == 504:
        r = yield get_tasks_request(bearer_token, limit, from_ts, sleep=DEFAULT_INTERVAL)
    j = try_json(r, status_code=200)
    try:
        return TaskList.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def _create_task_flow(bearer_token: str,
                      task_type: TaskType,
                      batch_size: int,
                      caption: Optional[str] = None,  # for 'text2im' and 'inpainting' task types
                      parent_id_or_image: Optional[str] = None,  # for 'variations' and 'inpainting' task types
                      masked_image: Optional[str] = None  # for 'inpainting' task type
                      ) -> HttpFlow[Task]:
    request = create_task_request(bearer_token, task_type,
                                  caption=caption, batch_size=batch_size,
                                  parent_id_or_image=parent_id_or_image,
                                  masked_image=masked_image)
    r = yield request
    while r.status_code == 504:
        request.sleep = DEFAULT_INTERVAL
        r = yield request
    j = try_json(r, status_code=200)
    try:
        return Task.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def create_text2im_task_flow(bearer_token: str, caption: str, batch_size: int = 4) -> HttpFlow[Task]:
    return _create_task_flow(bearer_token, caption=caption, task_type="text2im", batch_size=batch_size)


def create_variations_task_flow(bearer_token: str, parent_id_or_image: str, batch_size: int = 3) -> HttpFlow[Task]:
    return _create_task_flow(bearer_token, task_type="variations", batch_size=batch_size,
                             parent_id_or_image=parent_id_or_image)


def create_inpainting_task_flow(bearer_token: str, caption: str,
                                masked_image: str,
                                parent_id_or_image: Optional[str] = None,
                                batch_size: int = 3) -> HttpFlow[Task]:
    if parent_id_or_image is None:
        parent_id_or_image = masked_image
    return _create_task_flow(bearer_token,
                             task_type="inpainting",
                             batch_size=batch_size,
                             caption=caption,
                             parent_id_or_image=parent_id_or_image,
                             masked_image=masked_image)


def get_task_flow(bearer_token: str, task_id: str) -> HttpFlow[Task]:
    r = yield get_task_request(bearer_token, task_id=task_id)
    while r.status_code == 504:
        r = yield get_task_request(bearer_token, task_id=task_id, sleep=DEFAULT_INTERVAL)
    j = try_json(r, status_code=200)
    try:
        return Task.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def get_generation_flow(bearer_token: str, generation_id: str) -> HttpFlow[Generation]:
    r = yield get_generation_request(bearer_token, generation_id=generation_id)
    while r.status_code == 504:
        r = yield get_generation_request(bearer_token, generation_id=generation_id, sleep=DEFAULT_INTERVAL)
    j = try_json(r, status_code=200)
    try:
        return Generation.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def poll_for_task_completion_flow(bearer_token: str,
                                  task_id: str,
                                  interval: float = DEFAULT_INTERVAL,
                                  _max_attempts: int = 1000) -> HttpFlow[Task]:
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


def download_generation_flow(bearer_token: str, generation_id: str) -> HttpFlow[bytes]:
    r = yield download_generation_request(bearer_token, generation_id)
    while r.status_code == 504:
        r = yield download_generation_request(bearer_token, generation_id, sleep=DEFAULT_INTERVAL)
    if r.status_code != 200:
        raise FlowError("Failed to download generation", r)
    return r.content


def share_generation_flow(bearer_token: str, generation_id: str) -> HttpFlow[Generation]:
    r = yield share_generation_request(bearer_token, generation_id)
    while r.status_code == 504:
        r = yield share_generation_request(bearer_token, generation_id, sleep=DEFAULT_INTERVAL)
    if r.status_code != 200:
        raise FlowError("Failed to share generation", r)
    j = try_json(r, status_code=200)
    try:
        return Generation.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def flag_generation_flow(bearer_token: str, generation_id: str, description: str) -> HttpFlow[UserFlag]:
    r = yield flag_generation_request(bearer_token, generation_id, description)
    while r.status_code == 504:
        r = yield flag_generation_request(bearer_token, generation_id, description, sleep=DEFAULT_INTERVAL)
    if r.status_code != 200:
        raise FlowError("Failed to flag generation", r)
    j = try_json(r, status_code=200)
    try:
        return UserFlag.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def save_generations_flow(bearer_token: str, generation_ids: List[str],
                          collection_id_or_alias: str) -> HttpFlow[Collection]:
    if isinstance(generation_ids, str):
        generation_ids = [generation_ids]
    r = yield save_generations_request(bearer_token, generation_ids, collection_id_or_alias)
    while r.status_code == 504:
        r = yield save_generations_request(bearer_token, generation_ids, collection_id_or_alias, sleep=DEFAULT_INTERVAL)
    if r.status_code != 200:
        raise FlowError("Failed to save generations", r)
    j = try_json(r, status_code=200)
    try:
        return Collection.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e


def get_credit_summary_flow(bearer_token: str) -> HttpFlow[BillingInfo]:
    r = yield get_credit_summary_request(bearer_token)
    while r.status_code == 504:
        r = yield get_credit_summary_request(bearer_token, sleep=DEFAULT_INTERVAL)
    if r.status_code != 200:
        raise FlowError("Failed to get credit summary", r)
    j = try_json(r, status_code=200)
    try:
        return BillingInfo.from_dict(j)
    except Exception as e:
        raise FlowError("Failed to parse response", r) from e
