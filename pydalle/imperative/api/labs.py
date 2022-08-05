from typing import Optional, Dict, List

from pydalle.functional.api.response.labs import TaskList, Task, Generation, Collection, Login, UserFlag
from pydalle.functional.assumptions import OPENAI_AUTH0_DOMAIN, OPENAI_AUTH0_CLIENT_ID, \
    OPENAI_AUTH0_AUDIENCE, OPENAI_LABS_REDIRECT_URI, OPENAI_AUTH0_SCOPE
from pydalle.functional.api.flow.labs import get_bearer_token_flow, get_tasks_flow, get_task_flow, \
    create_text2im_task_flow, poll_for_task_completion_flow, create_variations_task_flow, \
    create_inpainting_task_flow, download_generation_flow, share_generation_flow, save_generations_flow, \
    get_login_info_flow, flag_generation_flow
from pydalle.imperative.api.auth0 import get_access_token_from_credentials, get_access_token_from_credentials_async
from pydalle.imperative.outside.internet import session_flow, session_flow_async

_LABS_AUTH0_PARAMS = {
    "domain": OPENAI_AUTH0_DOMAIN,
    "client_id": OPENAI_AUTH0_CLIENT_ID,
    "audience": OPENAI_AUTH0_AUDIENCE,
    "redirect_uri": OPENAI_LABS_REDIRECT_URI,
    "scope": OPENAI_AUTH0_SCOPE,
}


def get_access_token(username: str, password: str, headers: Optional[Dict[str, str]] = None) -> str:
    return get_access_token_from_credentials(username, password, **_LABS_AUTH0_PARAMS, headers=headers)


async def get_access_token_async(username: str, password: str,
                                 headers: Optional[Dict[str, str]] = None) -> str:
    return await get_access_token_from_credentials_async(username, password, **_LABS_AUTH0_PARAMS, headers=headers)


def get_bearer_token(username: str, password: str, headers: Optional[Dict[str, str]] = None) -> str:
    access_token = get_access_token_from_credentials(username, password, **_LABS_AUTH0_PARAMS, headers=headers)
    return session_flow(get_bearer_token_flow, headers, access_token=access_token)


async def get_bearer_token_async(username: str, password: str, headers: Optional[Dict[str, str]] = None) -> str:
    access_token = (
        await get_access_token_from_credentials_async(username, password, **_LABS_AUTH0_PARAMS, headers=headers))
    return await session_flow_async(get_bearer_token_flow, headers, access_token=access_token)


def get_login_info(access_token: str, headers: Optional[Dict[str, str]] = None) -> Login:
    return session_flow(get_login_info_flow, headers, access_token=access_token)


async def get_login_info_async(access_token: str, headers: Optional[Dict[str, str]] = None) -> Login:
    return await session_flow_async(get_login_info_flow, headers, access_token=access_token)


def get_bearer_token_from_access_token(access_token: str, headers: Optional[Dict[str, str]] = None) -> str:
    return session_flow(get_bearer_token_flow, headers, access_token=access_token)


async def get_bearer_token_from_access_token_async(access_token: str, headers: Optional[Dict[str, str]] = None) -> str:
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


def download_generation(bearer_token: str, generation_id: str, headers: Optional[Dict[str, str]] = None) -> bytes:
    return session_flow(download_generation_flow, headers, generation_id=generation_id, bearer_token=bearer_token)


async def download_generation_async(bearer_token: str, task_id: str, headers: Optional[Dict[str, str]] = None) -> bytes:
    return await session_flow_async(download_generation_flow, headers, task_id=task_id, bearer_token=bearer_token)


def share_generation(bearer_token: str, generation_id: str, headers: Optional[Dict[str, str]] = None) -> Generation:
    return session_flow(share_generation_flow, headers, generation_id=generation_id, bearer_token=bearer_token)


async def share_generation_async(bearer_token: str, generation_id: str,
                                 headers: Optional[Dict[str, str]] = None) -> Generation:
    return await session_flow_async(share_generation_flow, headers, generation_id=generation_id,
                                    bearer_token=bearer_token)


def save_generations(bearer_token: str, generation_ids: List[str], collection_id_or_alias="private",
                     headers: Optional[Dict[str, str]] = None) -> Collection:
    return session_flow(save_generations_flow, headers, collection_id_or_alias=collection_id_or_alias,
                        generation_ids=generation_ids, bearer_token=bearer_token)


async def save_generations_async(bearer_token: str, generation_ids: List[str], collection_id_or_alias="private",
                                 headers: Optional[Dict[str, str]] = None) -> Collection:
    return await session_flow_async(save_generations_flow, headers, collection_id_or_alias=collection_id_or_alias,
                                    generation_ids=generation_ids,
                                    bearer_token=bearer_token)


def _flag_generation(bearer_token: str, generation_id: str, description: str,
                     headers: Optional[Dict[str, str]] = None) -> UserFlag:
    return session_flow(flag_generation_flow, headers, generation_id=generation_id, reason=description,
                        bearer_token=bearer_token)


async def _flag_generation_async(bearer_token: str, generation_id: str, description: str,
                                 headers: Optional[Dict[str, str]] = None) -> UserFlag:
    return await session_flow_async(flag_generation_flow, headers, generation_id=generation_id, reason=description,
                                    bearer_token=bearer_token)


def flag_generation_sensitive(bearer_token: str, generation_id: str,
                              headers: Optional[Dict[str, str]] = None) -> UserFlag:
    return _flag_generation(bearer_token, generation_id, "Sensitive", headers)


async def flag_generation_sensitive_async(bearer_token: str, generation_id: str,
                                          headers: Optional[Dict[str, str]] = None) -> UserFlag:
    return await _flag_generation_async(bearer_token, generation_id, "Sensitive", headers)


def flag_generation_unexpected(bearer_token: str, generation_id: str,
                               headers: Optional[Dict[str, str]] = None) -> UserFlag:
    return _flag_generation(bearer_token, generation_id, "Unexpected", headers)


async def flag_generation_unexpected_async(bearer_token: str, generation_id: str,
                                           headers: Optional[Dict[str, str]] = None) -> UserFlag:
    return await _flag_generation_async(bearer_token, generation_id, "Unexpected", headers)
