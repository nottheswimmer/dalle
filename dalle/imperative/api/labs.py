from typing import Optional

from dalle.functional.api.response.labs import TaskList, Task
from dalle.functional.assumptions import OPENAI_AUTH0_DOMAIN, OPENAI_AUTH0_CLIENT_ID, \
    OPENAI_AUTH0_AUDIENCE, OPENAI_LABS_REDIRECT_URI, OPENAI_AUTH0_SCOPE
from dalle.functional.api.flow.labs import get_bearer_token_flow, get_tasks_flow, get_task_flow, \
    create_text2im_task_flow, poll_for_task_completion_flow
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


def get_tasks(bearer_token: str, from_ts: Optional[int] = None) -> TaskList:
    return session_flow(get_tasks_flow, from_ts=from_ts, bearer_token=bearer_token)


async def get_tasks_async(bearer_token: str, from_ts: Optional[int] = None) -> TaskList:
    return await session_flow_async(get_tasks_flow, from_ts=from_ts, bearer_token=bearer_token)


def get_task(bearer_token: str, task_id: str) -> Task:
    return session_flow(get_task_flow, task_id=task_id, bearer_token=bearer_token)


async def get_task_async(bearer_token: str, task_id: str) -> Task:
    return await session_flow_async(get_task_flow, task_id=task_id, bearer_token=bearer_token)


def create_text2im_task(bearer_token: str, caption: str, batch_size: int = 4) -> Task:
    return session_flow(create_text2im_task_flow, caption=caption, batch_size=batch_size, bearer_token=bearer_token)


async def create_text2im_task_async(bearer_token: str, caption: str, batch_size: int = 4) -> Task:
    return await session_flow_async(create_text2im_task_flow, caption=caption, batch_size=batch_size,
                                    bearer_token=bearer_token)


def poll_for_task_completion(bearer_token: str, task_id: str, interval: float = 1.0) -> Task:
    return session_flow(poll_for_task_completion_flow, task_id=task_id, bearer_token=bearer_token, interval=interval)


async def poll_for_task_completion_async(bearer_token: str, task_id: str, interval: float = 1.0) -> Task:
    return await session_flow_async(poll_for_task_completion_flow, task_id=task_id, bearer_token=bearer_token,
                                    interval=interval)
