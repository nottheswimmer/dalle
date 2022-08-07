import os
import asyncio
import platform

from pydalle.imperative.api.labs import get_bearer_token_async, get_tasks_async, poll_for_task_completion_async, \
    create_text2im_task_async, create_variations_task_async

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

OPENAI_USERNAME = os.environ['OPENAI_USERNAME']
OPENAI_PASSWORD = os.environ['OPENAI_PASSWORD']


async def main_async():
    print("Attempting to get token for DALL·E...")
    token = await get_bearer_token_async(OPENAI_USERNAME, OPENAI_PASSWORD)
    print("Token:", token)

    print("Attempting to check tasks...")
    tasks = await get_tasks_async(token)
    for task in tasks.data:
        print(task)
    print()

    print("Attempting to create text2im task...")
    pending_task = await create_text2im_task_async(token, "A cute cat")
    print(pending_task)
    print()

    print("Waiting for task to complete...")
    task = await poll_for_task_completion_async(token, pending_task.id)
    print(task)
    print()

    print("Attempting to create variations task...")
    pending_task = await create_variations_task_async(token, task.generations[0].id)
    print(pending_task)
    print()

    print("Waiting for task to complete...")
    task = await poll_for_task_completion_async(token, pending_task.id)
    print(task)
    print()

    # For additional examples, see dev.py and dev.ipynb


if __name__ == '__main__':
    asyncio.run(main_async())
