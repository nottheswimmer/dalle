# DALL-E 2 Python API Wrapper

This library provides basic programmatic access to the DALL-E 2 API.

The intent of this library is to provide researchers with a means to easily layout
results from DALL-E 2 into a jupyter notebook or similar.

## Tips

- Ensure your usage of DALL-E 2 abides by DALL-E 2's [content policy][1].

- Be mindful about how easy this library makes it for you to spend your money / DALL-E 2 credits.

- The primary benefit of this library over [ezzcodeezzlife/dalle2-in-python][2]
is that you do not need to manually paste in a session token and can just provide your username and password.

- If you wish to use this library in conjunction with the aforementioned library, you can do so by using the
get_bearer_token function from this library and passing the output to the [dalle2_in_python][2] library.

## Features

- get_bearer_token / get_bearer_token_async: Get a bearer token from username and password
- get_task / get_task_async: Get a task by ID
- get_tasks / get_tasks_async: Get tasks created after a given timestamp
- create_text2im_task / create_text2im_task_async: Create a task to generate an image from a text
- create_variations_task / create_variations_task_async: Create a task to generate variations of a generated image
- poll_for_task_completion / poll_for_task_completion_async: Poll for a task until it is complete

## Examples

See the following files for examples:
- dev.ipynb - Example of using the library in a jupyter notebook
- dev.py - Example of using the library in a python script
- dev_async.py - Example of using the library in a python script using asyncio

[1]: https://labs.openai.com/policies/content-policy
[2]: https://github.com/ezzcodeezzlife/dalle2-in-python
