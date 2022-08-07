from io import BytesIO

try:
    from PIL import Image as PILImage
except ImportError as e:
    from pydalle.functional.types import LazyImportError

    PILImage = LazyImportError("PIL.Image", e)
    del LazyImportError


def bytes_to_pil_image(image: bytes) -> PILImage:
    return PILImage.open(BytesIO(image))


def pil_image_to_png_bytes(image: PILImage) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def image_bytes_to_png_bytes(image: bytes) -> bytes:
    return pil_image_to_png_bytes(PILImage.open(BytesIO(image)))
