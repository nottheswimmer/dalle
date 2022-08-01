import os

from dalle.imperative.api.labs import get_bearer_token, get_tasks, create_text2im_task, poll_for_task_completion, \
    create_variations_task

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    print("Attempting to get token for DALL-E...")
    token = get_bearer_token(OPENAI_USERNAME, OPENAI_PASSWORD)
    print("Token:", token)

    print("Attempting to check tasks...")
    tasks = get_tasks(token)
    for task in tasks.data:
        print(task)
    print()

    print("Attempting to create text2im task...")
    pending_task = create_text2im_task(token, "A cute cat")
    print(pending_task)
    print()

    print("Waiting for task to complete...")
    task = poll_for_task_completion(token, pending_task.id)
    print(task)
    print()

    print("Attempting to create variations task...")
    pending_task = create_variations_task(token, task.generations[0].id)
    print(pending_task)
    print()

    print("Waiting for task to complete...")
    task = poll_for_task_completion(token, pending_task.id)
    print(task)
    print()


if __name__ == '__main__':
    main()
