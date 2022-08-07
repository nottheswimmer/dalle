# pydalle: A DALL·E 2 API Wrapper for Python

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydalle)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pydalle)
![PyPI - License](https://img.shields.io/pypi/l/pydalle)

This library provides basic programmatic access to the DALL·E 2 API.

The intent of this library is to provide researchers with a means to easily layout
results from DALL·E 2 into a jupyter notebook or similar.

pydalle has two main modes of use:

- **`pydalle.Dalle`**: This is the main class of the library. It provides a user-friendly
  interface to the DALL·E 2 API. [Read more here][4].
- **`pydalle.imperative.api.labs`**: This module provides a set of lower-level functions that
  can be used to interact with the DALL·E 2 API. [Read more here][5].

## Installation

### Install with all dependencies

    pip install pydalle[all]     # Install all dependencies, recommended for most users

### Pick and choose your dependencies

    pip install pydalle          # Just install the library with no optional dependencies
    pip install pydalle[sync]    # Also installs requests (for synchronous networking)
    pip install pydalle[async]   # Also installs aiohttp and aiofiles  (required for async networking / file handling)
    pip install pydalle[images]  # Also installs Pillow (required for help with image processing)

## Tips

- Get access by signing up for the [DALL·E 2 waitlist][1].

- Ensure your usage of DALL·E 2 abides by DALL·E 2's [content policy][2] and [terms of use][3].

- Be mindful about how easy this library makes it for you to spend your money / DALL·E 2 credits.

## Getting Started

Once you have installed pydalle, you can start using it by importing it and creating a `Dalle` object.
You can find all the available methods on the [Dalle class][4].

```python
import os

from pydalle import Dalle

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    client = Dalle(OPENAI_USERNAME, OPENAI_PASSWORD)
    print(f"Client created. {client.get_credit_summary().aggregate_credits} credits remaining...")
    tasks = client.get_tasks(limit=5)
    print(f"{len(tasks)} tasks found...")

    print("Attempting to do a text2im task...")
    completed_text2im_task = client.text2im("A cute cat")
    for image in completed_text2im_task.download():
        image.to_pil().show()

    print("Attempting to create variations task on the first cat...")
    first_generation = completed_text2im_task.generations[0]
    completed_variation_task = first_generation.variations()
    first_variation = completed_variation_task.generations[0]
    first_image = first_variation.download().to_pil()
    first_image.show()

    print("Attempting to create inpainting task and showing the mask...")
    # Make the right-side of the image transparent
    masked_image = first_image.convert("RGBA")
    for i in range(masked_image.width):
        if i > masked_image.width / 2:
            for j in range(masked_image.height):
                masked_image.putpixel((i, j), (0, 0, 0, 0))
    masked_image.show("inpainting mask")
    completed_inpainting_task = first_generation.inpainting("A cute cat, with a dark side", masked_image)
    for image in completed_inpainting_task.download():
        image.to_pil().show()


if __name__ == '__main__':
    main()
```

For an equivalent async code example, see [examples/dev_client_async.py](./examples/dev_client_async.py).

For examples of the low-level API and using this in a notebook, see 
  the [examples/low_level](./examples/low_level) directory.

[1]: https://labs.openai.com/waitlist

[2]: https://labs.openai.com/policies/content-policy

[3]: https://labs.openai.com/policies/terms

[4]: https://pydalle.readthedocs.io/en/latest/pydalle.imperative.client.html#pydalle.imperative.client.dalle.Dalle

[5]: https://pydalle.readthedocs.io/en/latest/pydalle.imperative.api.html#module-pydalle.imperative.api.labs