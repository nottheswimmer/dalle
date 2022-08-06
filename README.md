# pydalle: A DALL·E 2 API Wrapper for Python

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydalle)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pydalle)
![PyPI - License](https://img.shields.io/pypi/l/pydalle)

This library provides basic programmatic access to the DALL·E 2 API.

The intent of this library is to provide researchers with a means to easily layout
results from DALL·E 2 into a jupyter notebook or similar.

Read the documentation for pydalle on [readthedocs](https://pydalle.readthedocs.io/en/latest/pydalle.imperative.api.html?#module-pydalle.imperative.api.labs).

## Installation

    pip install pydalle

If you want to use sync methods, also make sure you have the `requests` library installed.

    pip install requests

If you want to use async methods, also make sure you have the `aiohttp` library installed.

    pip install aiohttp

## Tips

- Get access by signing up for the [DALL·E 2 waitlist][1].

- Ensure your usage of DALL·E 2 abides by DALL·E 2's [content policy][2] and [terms of use][3].

- Be mindful about how easy this library makes it for you to spend your money / DALL·E 2 credits.

## Features

- `get_bearer_token` / `get_bearer_token_async`: Get a bearer token from username and password (discards access token)
- `get_task` / `get_task_async`: Get a task by ID
- `get_tasks` / `get_tasks_async`: Get tasks created after a given timestamp
- `create_text2im_task` / `create_text2im_task_async`: Create a task to generate an image from a text
- `create_variations_task` / `create_variations_task_async`: Create a task to generate variations of an image
- `create_inpainting_task` / `create_inpainting_task_async`: Create a task to generate an image from a mask and caption
- `poll_for_task_completion /` `poll_for_task_completion_async`: Poll for a task until it is complete
- `download_generation` / `download_generation_async`: Download the image bytes for a given generation ID
  (the generation also has an image_path field, but it does not include the necessary watermark so use this instead)
- `share_generation` / `share_generation_async`: Make the generation with the given ID public. The share_url property on the returned object 
   will include the share link for this image
- `save_generations / save_generations_async`: Save the generations with the given generation IDs to your collection. Returns a
    Collection object for the collection saved to.
- `flag_generation_sensitive / flag_generation_sensitive_async`: Flag a generation as sensitive. Returns a
    UserFlag object with details about the flag.
- `flag_generation_unexpected / flag_generation_unexpected_async`: Flag a generation as unexpected. Returns a
    UserFlag object with details about the flag.
- `get_credit_summary / get_credit_summary_async`: Get a summary of your DALL·E 2 billing information.
- `get_access_token` / `get_access_token_async`: Get an access token from username and password. Only needed for the following:
  - `get_bearer_token_with_access_token` / `get_bearer_token_with_access_token_async`: Get a bearer token from an access token.
  - `get_login_info` / `get_login_info_async`: Get information for the user (which includes the bearer token).

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

## Useful tools

While not dependencies of this library, the following tools are useful companions when working with images:

- PIL: `pip install Pillow`
    - Displaying an image in a notebook or in a Python script
    - Adding an alpha channel to an image (for creating masks)
    - Converting an image to PNG format (for uploading to DALL·E 2)
    - Resizing, cropping, padding, and masking images (etc.)
    - Saving images to disk
- matplotlib: `pip install matplotlib`
    - Arranging images in a grid for display
- numpy: `pip install numpy`
    - Vectorization of image processing operations
      (if you find yourself doing a lot of slow loops over pixels, try putting the image in a numpy array and
      vectorizing the loops)

[1]: https://labs.openai.com/waitlist

[2]: https://labs.openai.com/policies/content-policy

[3]: https://labs.openai.com/policies/terms
