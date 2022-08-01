import os

from dalle.imperative.api.labs import get_bearer_token, get_tasks, create_text2im_task, poll_for_task_completion

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    print("Attempting to get token for DALL-E...")
    token = get_bearer_token(OPENAI_USERNAME, OPENAI_PASSWORD)
    print("Token:", token)

    print("Attempting to check tasks...")
    tasks = get_tasks(token)
    for task in tasks.data:
        print(task.id, task.status, task.generations)

    print("Attempting to create task...")
    pending_task = create_text2im_task(token, "A cute cat")
    print(pending_task.id, pending_task.status, pending_task.generations)
    print("Waiting for task to complete...")
    task = poll_for_task_completion(token, pending_task.id)
    print(task.id, task.status, task.generations)


if __name__ == '__main__':
    main()
