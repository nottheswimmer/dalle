from typing import Optional, Dict

from pydalle.functional.api.response.labs import TaskList, Task
from pydalle.functional.assumptions import OPENAI_AUTH0_DOMAIN, OPENAI_AUTH0_CLIENT_ID, \
    OPENAI_AUTH0_AUDIENCE, OPENAI_LABS_REDIRECT_URI, OPENAI_AUTH0_SCOPE
from pydalle.functional.api.flow.labs import get_bearer_token_flow, get_tasks_flow, get_task_flow, \
    create_text2im_task_flow, poll_for_task_completion_flow, create_variations_task_flow, create_inpainting_task_flow
from pydalle.imperative.api.auth0 import get_access_token, get_access_token_async
from pydalle.imperative.outside.internet import session_flow, session_flow_async

_LABS_AUTH0_PARAMS = {
    "domain": OPENAI_AUTH0_DOMAIN,
    "client_id": OPENAI_AUTH0_CLIENT_ID,
    "audience": OPENAI_AUTH0_AUDIENCE,
    "redirect_uri": OPENAI_LABS_REDIRECT_URI,
    "scope": OPENAI_AUTH0_SCOPE,
}


def get_bearer_token(username: str, password: str, headers: Optional[Dict[str, str]] = None) -> str:
    access_token = get_access_token(username, password, **_LABS_AUTH0_PARAMS, headers=headers)
    return session_flow(get_bearer_token_flow, headers, access_token=access_token)


async def get_bearer_token_async(username: str, password: str, headers: Optional[Dict[str, str]] = None) -> str:
    access_token = (await get_access_token_async(username, password, **_LABS_AUTH0_PARAMS, headers=headers))
    return await session_flow_async(get_bearer_token_flow, headers, access_token=access_token)


def get_tasks(bearer_token: str, from_ts: Optional[int] = None, headers: Optional[Dict[str, str]] = None) -> TaskList:
    return session_flow(get_tasks_flow, headers, from_ts=from_ts, bearer_token=bearer_token)


async def get_tasks_async(bearer_token: str, from_ts: Optional[int] = None,
                          headers: Optional[Dict[str, str]] = None) -> TaskList:
    return await session_flow_async(get_tasks_flow, headers, from_ts=from_ts, bearer_token=bearer_token)


def get_task(bearer_token: str, task_id: str, headers: Optional[Dict[str, str]] = None) -> Task:
    return session_flow(get_task_flow, headers, task_id=task_id, bearer_token=bearer_token)


async def get_task_async(bearer_token: str, task_id: str, headers: Optional[Dict[str, str]] = None) -> Task:
    return await session_flow_async(get_task_flow, headers, task_id=task_id, bearer_token=bearer_token)


def create_text2im_task(bearer_token: str, caption: str, batch_size: int = 4,
                        headers: Optional[Dict[str, str]] = None) -> Task:
    return session_flow(create_text2im_task_flow, headers, caption=caption, batch_size=batch_size,
                        bearer_token=bearer_token)


async def create_text2im_task_async(bearer_token: str, caption: str, batch_size: int = 4,
                                    headers: Optional[Dict[str, str]] = None) -> Task:
    return await session_flow_async(create_text2im_task_flow, headers, caption=caption, batch_size=batch_size,
                                    bearer_token=bearer_token)


def create_variations_task(bearer_token: str, parent_id_or_image: str, batch_size: int = 3,
                           headers: Optional[Dict[str, str]] = None) -> Task:
    return session_flow(create_variations_task_flow, headers, parent_id_or_image=parent_id_or_image,
                        batch_size=batch_size, bearer_token=bearer_token)


async def create_variations_task_async(bearer_token: str, parent_id_or_image: str,
                                       batch_size: int = 3, headers: Optional[Dict[str, str]] = None) -> Task:
    return await session_flow_async(create_variations_task_flow, headers,
                                    parent_id_or_image=parent_id_or_image,
                                    batch_size=batch_size, bearer_token=bearer_token)


def create_inpainting_task(bearer_token: str, caption: str, masked_image: str, parent_id_or_image: Optional[str] = None,
                           batch_size: int = 3, headers: Optional[Dict[str, str]] = None) -> Task:
    return session_flow(create_inpainting_task_flow, headers, caption=caption, parent_id_or_image=parent_id_or_image,
                        masked_image=masked_image, batch_size=batch_size, bearer_token=bearer_token)


async def create_inpainting_task_async(bearer_token: str, caption: str, masked_image: str,
                                       parent_id_or_image: Optional[str] = None, batch_size: int = 3,
                                       headers: Optional[Dict[str, str]] = None) -> Task:
    return await session_flow_async(create_inpainting_task_flow, headers, caption=caption,
                                    parent_id_or_image=parent_id_or_image, masked_image=masked_image,
                                    batch_size=batch_size, bearer_token=bearer_token)


def poll_for_task_completion(bearer_token: str, task_id: str, interval: float = 1.0,
                             headers: Optional[Dict[str, str]] = None) -> Task:
    return session_flow(poll_for_task_completion_flow, headers, task_id=task_id, bearer_token=bearer_token,
                        interval=interval)


async def poll_for_task_completion_async(bearer_token: str, task_id: str, interval: float = 1.0,
                                         headers: Optional[Dict[str, str]] = None) -> Task:
    return await session_flow_async(poll_for_task_completion_flow, headers, task_id=task_id, bearer_token=bearer_token,
                                    interval=interval)
