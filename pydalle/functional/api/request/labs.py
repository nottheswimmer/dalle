"""
This module contains functions which are used to construct requests to the OpenAI Labs API.
"""

import json
from typing import Optional, List

from pydalle.functional.api.response.labs import TaskType
from pydalle.functional.assumptions import OPENAI_LABS_TASKS_URL, OPENAI_LABS_LOGIN_URL, \
    OPENAI_LABS_TASK_URL_TEMPLATE,OPENAI_LABS_GENERATION_URL_TEMPLATE,  OPENAI_LABS_GENERATION_DOWNLOAD_URL_TEMPLATE, \
    OPENAI_LABS_GENERATION_SHARE_URL_TEMPLATE, OPENAI_LABS_COLLECTION_GENERATION_URL_TEMPLATE, \
    OPENAI_LABS_GENERATION_FLAG_URL_TEMPLATE, OPENAI_LABS_BILLING_CREDIT_SUMMARY_URL
from pydalle.functional.types import HttpRequest
from pydalle.functional.utils import filter_none


def get_task_request(bearer_token: str, task_id: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_TASK_URL_TEMPLATE % task_id,
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       sleep=sleep)


def get_tasks_request(bearer_token: str, limit: Optional[int] = None, from_ts: Optional[int] = None, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_TASKS_URL,
                       params=filter_none({"from_ts": from_ts, "limit": limit}),
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       sleep=sleep)


def get_generation_request(bearer_token: str, generation_id: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_GENERATION_URL_TEMPLATE % generation_id,
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


def download_generation_request(bearer_token: str, generation_id: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_GENERATION_DOWNLOAD_URL_TEMPLATE % generation_id,
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       decode=False,
                       sleep=sleep)


def share_generation_request(bearer_token: str, generation_id: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="post",
                       url=OPENAI_LABS_GENERATION_SHARE_URL_TEMPLATE % generation_id,
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       sleep=sleep)


def save_generations_request(bearer_token: str, generation_ids: List[str], collection_id_or_alias: str,
                             sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="post",
                       url=OPENAI_LABS_COLLECTION_GENERATION_URL_TEMPLATE % collection_id_or_alias,
                       data=json.dumps({"generation_ids": generation_ids}),
                       headers={"Authorization": f"Bearer {bearer_token}",
                                "Content-Type": "application/json"},
                       sleep=sleep)


def flag_generation_request(bearer_token: str, generation_id: str, description: str,
                            sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="post",
                       url=OPENAI_LABS_GENERATION_FLAG_URL_TEMPLATE % generation_id,
                       data=json.dumps({"description": description}),
                       headers={"Authorization": f"Bearer {bearer_token}",
                                "Content-Type": "application/json"},
                       sleep=sleep)


def get_credit_summary_request(bearer_token: str, sleep: Optional[float] = None) -> HttpRequest:
    return HttpRequest(method="get",
                       url=OPENAI_LABS_BILLING_CREDIT_SUMMARY_URL,
                       headers={"Authorization": f"Bearer {bearer_token}"},
                       sleep=sleep)


def _classify_image_parameter(parent_id_or_image):
    if parent_id_or_image is not None:
        if parent_id_or_image.startswith("generation-"):
            return "parent_generation_id"
        elif parent_id_or_image.startswith("prompt-"):
            return "parent_prompt_id"
    return "image"
