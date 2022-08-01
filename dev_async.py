import os
import asyncio
import platform

from dalle.imperative.api.labs import get_bearer_token_async, get_tasks_async, poll_for_task_completion_async, \
    create_text2im_task_async

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

OPENAI_USERNAME = os.environ['OPENAI_USERNAME']
OPENAI_PASSWORD = os.environ['OPENAI_PASSWORD']


async def main_async():
    print("Attempting to get token for DALL-E...")
    token = await get_bearer_token_async(OPENAI_USERNAME, OPENAI_PASSWORD)
    print("Token:", token)
    print("Attempting to check tasks...")
    tasks = await get_tasks_async(token)
    for task in tasks:
        print(task.status, task.id, task.prompt_id, task.created)
    print("Attempting to create task...")
    pending_task = await create_text2im_task_async(token, "A cute cat")
    print(pending_task.id, pending_task.status, pending_task.generations)
    print("Waiting for task to complete...")
    task = await poll_for_task_completion_async(token, pending_task.id)
    print(task.id, task.status, task.generations)


if __name__ == '__main__':
    asyncio.run(main_async())
