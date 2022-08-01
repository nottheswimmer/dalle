import os
from io import BytesIO
from urllib.request import urlopen

import base64
from PIL import Image

from pydalle.imperative.api.labs import get_bearer_token, get_tasks, create_text2im_task, poll_for_task_completion, \
    create_variations_task, create_inpainting_task

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    print("Attempting to get token for DALL·E...")
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

    task = wait_for_task(pending_task, token)
    download_and_show(task)

    print("Attempting to create variations task...")
    pending_task = create_variations_task(token, task.generations[0].id)
    print(pending_task)
    print()

    task = wait_for_task(pending_task, token)
    image = download_and_show(task)

    print("Attempting to create inpainting task and showing the mask...")
    # Make the right-side of the image transparent
    image = image.convert("RGBA")
    for i in range(image.width):
        if i > image.width / 2:
            for j in range(image.height):
                image.putpixel((i, j), (0, 0, 0, 0))
    image.show("inpainting mask")
    # Convert image to a base64 png string
    with BytesIO() as buffer:
        image.save(buffer, format="PNG")
        base64_png = base64.b64encode(buffer.getvalue()).decode()
    pending_task = create_inpainting_task(token,
                                          caption="A cute cat, with a dark side",
                                          masked_image=base64_png,
                                          parent_id_or_image=task.generations[0].id)
    print(pending_task)
    print()

    task = wait_for_task(pending_task, token)

    download_and_show(task)


def wait_for_task(pending_task, token):
    print("Waiting for task to complete...")
    task = poll_for_task_completion(token, pending_task.id)
    print(task)
    print()
    return task


def download_and_show(task):
    print("Attempting to download first generated image and show...")
    image_path = task.generations[0].generation.image_path
    print("Image path:", image_path)
    image = Image.open(urlopen(image_path))
    image.show("generated image")
    print()
    return image


if __name__ == '__main__':
    main()
