import json
from typing import Optional

from dalle.functional.api.response.labs import TaskType
from dalle.functional.assumptions import OPENAI_LABS_TASKS_URL, OPENAI_LABS_LOGIN_URL, OPENAI_LABS_TASK_URL_TEMPLATE
from dalle.functional.types import HttpRequest
from dalle.functional.utils import filter_none


def get_task_request(bearer_token: str, task_id: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_TASK_URL_TEMPLATE % task_id,
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       sleep=sleep)


def get_tasks_request(bearer_token: str, from_ts: Optional[int] = None, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_TASKS_URL,
                       params=filter_none({"from_ts": from_ts}),
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       sleep=sleep)


def login_request(access_token: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="post", url=OPENAI_LABS_LOGIN_URL, headers={"Authorization": f"Bearer {access_token}"},
                       sleep=sleep)


def create_task_request(bearer_token: str,
                        task_type: TaskType,
                        batch_size: int,
                        caption: Optional[str] = None,
                        parent_id_or_image: Optional[str] = None,
                        masked_image: Optional[str] = None,
                        sleep: Optional[float] = None) -> HttpRequest:
    image_key = _classify_image_parameter(parent_id_or_image)
    return HttpRequest(method="post",
                       url=OPENAI_LABS_TASKS_URL,
                       data=json.dumps(
                           filter_none(
                               {"task_type": task_type, "prompt":
                                   filter_none({"caption": caption,
                                                "batch_size": batch_size,
                                                image_key: parent_id_or_image,
                                                "masked_image": masked_image})})
                       ),
                       headers={"Authorization": f"Bearer {bearer_token}",
                                "Content-Type": "application/json"},
                       sleep=sleep)


def _classify_image_parameter(parent_id_or_image):
    if parent_id_or_image is not None:
        if parent_id_or_image.startswith("generation-"):
            return "parent_generation_id"
        elif parent_id_or_image.startswith("prompt-"):
            return "parent_prompt_id"
    return "image"
