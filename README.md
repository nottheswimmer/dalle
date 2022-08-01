# pydalle: A DALL-E 2 API Wrapper for Python

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydalle)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pydalle)
![PyPI - License](https://img.shields.io/pypi/l/pydalle)

This library provides basic programmatic access to the DALL-E 2 API.

The intent of this library is to provide researchers with a means to easily layout
results from DALL-E 2 into a jupyter notebook or similar.

## Installation

    pip install pydalle

If you want to use sync methods, also make sure you have the `requests` library installed.

    pip install requests

If you want to use async methods, also make sure you have the `aiohttp` library installed.

    pip install aiohttp

While not required, the PIL library is also recommended for image processing.

    pip install Pillow

## Tips

- Ensure your usage of DALL-E 2 abides by DALL-E 2's [content policy][1].

- Be mindful about how easy this library makes it for you to spend your money / DALL-E 2 credits.

- The primary benefit of our library over [ezzcodeezzlife/dalle2-in-python][2]
  is that you do not need to manually paste in a session token and can just provide your username and password.
  For a few people, our optional asyncio support might also be a plus.

## Features

- `get_bearer_token` / `get_bearer_token_async`: Get a bearer token from username and password
- `get_task` / `get_task_async`: Get a task by ID
- `get_tasks` / `get_tasks_async`: Get tasks created after a given timestamp
- `create_text2im_task` / `create_text2im_task_async`: Create a task to generate an image from a text
- `create_variations_task` / `create_variations_task_async`: Create a task to generate variations of a generated image
- `create_variations_task` / `create_inpainting_task_async`: Create a task to generate an image from a mask
- `poll_for_task_completion /` `poll_for_task_completion_async`: Poll for a task until it is complete

## Image input

All the following notes on method usage also apply to each method's corresponding async version.

- `create_variations_task` and `create_inpainting_task` both accept a parameter called `parent_id_or_image`.
    - For `create_variations_task`, it is required.
    - For `create_inpainting_task`, it will default to the value of the image_mask parameter if not provided.
    - It can be a string in any of the following formats:
        - A "generation ID" (format: `generation-[a-zA-Z0-9]{24}`) -- can be obtained with prefix included from a task
          with `task.generations[i].id`
        - A "prompt ID" (format: `prompt-[a-zA-Z0-9]{24}`) -- can be obtained with prefix included from a task
          with `task.prompt_id or task.prompt.id`
        - A base64-encoded PNG image decoded as a string -- full examples in `dev.ipynb` and `dev.py`
- `create_inpainting_task` also accepts the parameter `image_mask`
    - It must be a base64-encoded PNG image decoded as a string -- full examples in `dev.ipynb` and `dev.py`

## Examples

See the following files for examples:

- [dev.ipynb](./dev.ipynb) - Example of using the library in a jupyter notebook
- [dev.py](./dev.py) - Example of using the library in a python script
- [dev_async.py](./dev_async.py) - Example of using the library in a python script using asyncio

[1]: https://labs.openai.com/policies/content-policy
[2]: https://github.com/ezzcodeezzlife/dalle2-in-python
[requests]: https://requests.readthedocs.io/en/master/