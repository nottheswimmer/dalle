"""
This module contains all functions pydalle uses to directly interface with PIL.
"""

from io import BytesIO

try:
    from PIL import Image as PILImage
except ImportError as e:
    from pydalle.functional.types import LazyImportError

    PILImage = LazyImportError("PIL.Image", e)
    del LazyImportError

PILImageType = type(PILImage)


def bytes_to_pil_image(image: bytes) -> PILImageType:
    return PILImage.open(BytesIO(image))


def pil_image_to_png_bytes(image: PILImageType) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def image_bytes_to_png_bytes(image: bytes) -> bytes:
    return pil_image_to_png_bytes(PILImage.open(BytesIO(image)))


def bytes_to_masked_pil_image(image: bytes, x1: float, y1: float, x2: float, y2: float) -> PILImageType:
    image = bytes_to_pil_image(image).convert("RGBA")
    x1 = int(x1 * image.width)
    y1 = int(y1 * image.height)
    x2 = int(x2 * image.width)
    y2 = int(y2 * image.height)
    image.paste(PILImage.new("RGBA", (x2 - x1, y2 - y1), (0, 0, 0, 0)), (x1, y1))
    return image


def bytes_to_padded_pil_image(image: bytes, p: float, cx: float = 0.5, cy: float = 0.5) -> PILImageType:
    """
    Shrinks an image by a given percentage. The actual image size does not change,
    but the image is scaled down by the given percentage and a transparent border
    is added to the edges.
    """
    old_image = bytes_to_pil_image(image).convert("RGBA")
    new_image = PILImage.new("RGBA", (old_image.width, old_image.height), (0, 0, 0, 0))
    old_image = old_image.resize((int(old_image.width * p), int(old_image.height * p)),
                                    resample=PILImage.LANCZOS)
    new_image.paste(old_image, (int((new_image.width - old_image.width) * cx),
                                int((new_image.height - old_image.height) * cy)))
    return new_image