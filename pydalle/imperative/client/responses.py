import base64
import asyncio
from functools import cached_property
from typing import Optional, List, Iterator, TYPE_CHECKING, Any, Union, Generator, AsyncGenerator

from pydalle.functional.api.response.labs import TaskList, Task, Generation, Collection, UserFlag, BillingInfo, \
    TaskType, Prompt, StatusInformation, GenerationData, Breakdown, Login, User, Features, GenerationList
from pydalle.functional.types import HttpRequest, T
from pydalle.imperative.outside import files
from pydalle.imperative.outside.internet import request, request_async
from pydalle.imperative.outside.pil import PILImageType, pil_image_to_png_bytes, image_bytes_to_png_bytes, \
    bytes_to_pil_image, bytes_to_masked_pil_image, bytes_to_padded_pil_image
from pydalle.imperative.outside.np import ndarray, pil_image_to_np_array, np_array_to_pil_image

if TYPE_CHECKING:
    from pydalle.imperative.client.dalle import Dalle

PNG_PREFIX = b"\x89PNG\r\n\x1a\n"
PNG_BASE64_PREFIX = b"iVBORw0KGgo"
PNG_BASE64_PREFIX_STR = PNG_BASE64_PREFIX.decode()


class WrappedResponse:
    """
    Generic wrapper for responses from the Dalle API. This has the following benefits:

    * The dalle client is passed in as an argument to the constructor, so that the client can be used to
        make requests related to the wrapped response.

    * Getters for attributes in the lower-level response helps protect against changes in the API.
    """

    def __init__(self, wrapped: T, dalle: 'Dalle'):
        self.wrapped: T = wrapped
        self.dalle = dalle

    def __repr__(self):
        return f"{self.__class__.__name__}({self.wrapped!r})"


class WrappedTaskList(WrappedResponse):
    wrapped: TaskList

    def __init__(self, task_list: TaskList, dalle: 'Dalle'):
        super().__init__(task_list, dalle)

    def __iter__(self) -> Iterator['WrappedTask']:
        yield from (WrappedTask(task, self.dalle) for task in self.wrapped)

    def __getitem__(self, index) -> 'WrappedTask':
        return WrappedTask(self.wrapped[index], self.dalle)

    def __len__(self) -> int:
        return len(self.wrapped)


class WrappedTask(WrappedResponse):
    wrapped: Task

    def __init__(self, task: Task, dalle: 'Dalle'):
        super().__init__(task, dalle)

    @property
    def id(self) -> str:
        return self.wrapped.id

    @property
    def created(self) -> int:
        return self.wrapped.created

    @property
    def task_type(self) -> TaskType:
        return self.wrapped.task_type

    @property
    def status(self) -> str:
        return self.wrapped.status

    @property
    def status_information(self) -> 'StatusInformation':
        return self.wrapped.status_information

    @property
    def prompt_id(self) -> str:
        return self.wrapped.prompt_id

    @property
    def generations(self) -> Optional['WrappedGenerationList']:
        if self.wrapped.generations is None:
            return None
        return WrappedGenerationList(self.wrapped.generations, self.dalle)

    @property
    def prompt(self) -> 'Prompt':
        return self.wrapped.prompt

    @property
    def succeeded(self) -> bool:
        return self.wrapped.status == 'succeeded'

    @property
    def pending(self) -> bool:
        return self.wrapped.status == 'pending'

    @property
    def rejected(self) -> bool:
        return self.wrapped.status == 'rejected'

    def download(self, direct=False) -> Generator['WrappedImage', None, None]:
        yield from (generation.download(direct=direct) for generation in self.generations)

    async def download_async(self, direct=False) -> AsyncGenerator['WrappedImage', None]:
        download_tasks = [generation.download_async(direct=direct) for generation in self.generations]
        for download_task in asyncio.as_completed(download_tasks):
            yield await download_task

    def wait(self) -> 'WrappedTask':
        return self.dalle.poll_for_task_completion(self.id)

    async def wait_async(self) -> 'WrappedTask':
        return await self.dalle.poll_for_task_completion_async(self.id)


class WrappedGenerationList:
    wrapped: GenerationList

    def __init__(self, generation_list: GenerationList, dalle: 'Dalle'):
        self.wrapped = generation_list
        self.dalle = dalle

    def __iter__(self) -> Iterator['WrappedGeneration']:
        yield from (WrappedGeneration(generation, self.dalle) for generation in self.wrapped)

    def __getitem__(self, index) -> 'WrappedGeneration':
        return WrappedGeneration(self.wrapped[index], self.dalle)

    def __len__(self) -> int:
        return len(self.wrapped)


class WrappedGeneration(WrappedResponse):
    wrapped: Generation

    def __init__(self, generation: Generation, dalle: 'Dalle'):
        super().__init__(generation, dalle)

    @property
    def id(self) -> str:
        return self.wrapped.id

    @property
    def created(self) -> int:
        return self.wrapped.created

    @property
    def generation_type(self) -> str:
        return self.wrapped.generation_type

    @property
    def generation(self) -> 'GenerationData':
        return self.wrapped.generation

    @property
    def task_id(self) -> str:
        return self.wrapped.task_id

    @property
    def prompt_id(self) -> str:
        return self.wrapped.prompt_id

    @property
    def is_public(self) -> bool:
        return self.wrapped.is_public

    @property
    def direct_image_path(self) -> str:
        return self.generation.image_path

    def download(self, direct=False) -> 'WrappedImage':
        return self.dalle.download_generation(self, direct=direct)

    def variations(self, wait=True):
        return self.dalle.variations(self, wait=wait)

    def inpainting(self, caption: str, masked_image: 'ImageLike', wait=True):
        return self.dalle.inpainting(caption=caption, masked_image=masked_image, wait=wait)

    async def download_async(self, direct=False) -> 'WrappedImage':
        return await self.dalle.download_generation_async(self, direct=direct)

    async def variations_async(self, wait=True):
        return await self.dalle.variations_async(self, wait=wait)

    async def inpainting_async(self, caption: str, masked_image: 'ImageLike', wait=True):
        return await self.dalle.inpainting_async(caption=caption, masked_image=masked_image, wait=wait)


GenerationLike = Union[WrappedGeneration, Generation, str]


def get_generation_id(generation: GenerationLike) -> str:
    if isinstance(generation, (WrappedGeneration, Generation)):
        return generation.id
    if not str(generation).startswith("generation-"):
        raise ValueError("Unrecognized generation: {}".format(generation))
    return str(generation)


TaskLike = Union[WrappedTask, Task, str]


def get_task_id(task: TaskLike) -> str:
    if isinstance(task, (WrappedTask, Task)):
        return task.id
    if not str(task).startswith("task-"):
        raise ValueError("Unrecognized task: {}".format(task))
    return str(task)


class WrappedCollection(WrappedResponse):
    wrapped: Collection

    def __init__(self, collection: Collection, dalle: 'Dalle'):
        super().__init__(collection, dalle)

    @property
    def id(self) -> str:
        return self.wrapped.id

    @property
    def created(self) -> int:
        return self.wrapped.created

    @property
    def name(self) -> str:
        return self.wrapped.name

    @property
    def description(self) -> str:
        return self.wrapped.description

    @property
    def is_public(self) -> bool:
        return self.wrapped.is_public

    @property
    def alias(self) -> str:
        return self.wrapped.alias


class WrappedImage(WrappedResponse):
    wrapped: bytes

    def __init__(self, image: bytes, dalle: 'Dalle', filetype: str = 'png'):
        super().__init__(image, dalle)
        self.filetype = filetype.lower()

    def __bytes__(self):
        return self.png_bytes

    @cached_property
    def png_bytes(self) -> bytes:
        if self.filetype == 'png':
            return self.wrapped
        return image_bytes_to_png_bytes(self.wrapped)

    def to_pil(self) -> PILImageType:
        """
        Returns a PIL image object for the image.

        :return: A PIL image object.
        """
        return bytes_to_pil_image(bytes(self))

    def to_numpy(self) -> ndarray:
        """
        Returns a numpy array for the image.

        :return: A numpy array.
        """
        return pil_image_to_np_array(self.to_pil())

    def to_pil_masked(self, x1: float, y1: float, x2: float, y2: float) -> PILImageType:
        """
        Returns a PIL image object for the image, with the given mask applied.

        :param x1: The percentage of the image on the left before the mask starts.
        :param y1: The percentage of the image on the top before the mask starts.
        :param x2: The percentage of the image on the right after the mask ends.
        :param y2: The percentage of the image on the bottom after the mask ends.

        :return: A masked PIL image object.
        """
        return bytes_to_masked_pil_image(bytes(self), x1, y1, x2, y2)

    def to_pil_padded(self, p: float, cx: float = 0.5, cy: float = 0.5) -> PILImageType:
        """
        Returns a PIL image object for the image, with the given padding applied.

        :param p: The percentage of the image to pad. E.g. 0.5 means the image will be shrunk by 50%.
        :param cx: Where the newly shrunk image will be centered horizontally. Default is 0.5, the center.
        :param cy: Where the newly shrunk image will be centered vertically. Default is 0.5, the center.
        :return: A padded PIL image object.
        """
        return bytes_to_padded_pil_image(bytes(self), p, cx, cy)


PromptLike = Union[Prompt, str]

ImageLike = Union[WrappedImage, PILImageType, bytes, str]
ParentLike = Union[ImageLike, GenerationLike, PromptLike]


def _get_image_png_base64_no_io(image: ImageLike) -> str:
    if isinstance(image, str):
        if image.startswith(PNG_BASE64_PREFIX.decode()):
            # If it's already a base64 encoded PNG, we're good
            return image
        try:
            # If it's a base64 encoded string in the wrong format, we'll try the PIL trick
            decoded = base64.b64decode(image)
            if image == base64.b64encode(decoded).decode():
                return base64.b64encode(image_bytes_to_png_bytes(decoded)).decode()
        except ValueError:
            pass
    if isinstance(image, WrappedImage):
        return base64.b64encode(image.png_bytes).decode()
    if isinstance(image, bytes):
        if image.startswith(PNG_BASE64_PREFIX):
            # If it's already a base64 encoded PNG, we just need to decode it
            return image.decode()
        elif image.startswith(PNG_PREFIX):
            # If it's a PNG bytes, we'll base64 encode it
            return base64.b64encode(image).decode()
        # Check if the bytes are base64 encoded. If it is,
        # we'll assume it's an image in another format base64 encoded
        try:
            decoded = base64.b64decode(image)

            if image == base64.b64encode(decoded):
                image = decoded
        except ValueError:
            pass
        # So, now it's bytes that are not a PNG or base64 encoded PNG.
        # Best guess is that it's an image of some other format.
        # If the user has PIL installed, we'll try to convert it to PNG
        return base64.b64encode(image_bytes_to_png_bytes(image)).decode()
    try:
        if isinstance(image, ndarray):
            return base64.b64encode(pil_image_to_png_bytes(np_array_to_pil_image(image))).decode()
    except ImportError:
        pass
    try:
        if str(image.__class__).startswith("<class 'PIL."):
            # If it's a PIL image, we'll make sure it's a PNG and return the base64
            return base64.b64encode(pil_image_to_png_bytes(image)).decode()
    except ImportError:
        pass


def get_image_png_base64(image: ImageLike, headers: Optional[dict]) -> str:
    if result := _get_image_png_base64_no_io(image):
        return result
    # Maybe it's a URL?
    if (lower := image.lower()).startswith("http://") or lower.startswith("https://"):
        # If it's a URL, we'll try to download it
        r = request(HttpRequest("get", image, headers=headers, decode=False))
        if r.status_code == 200:
            return get_image_png_base64(r.content, headers)
        raise ValueError(f"Could not download image: {image}")
    # Maybe it's a file path?
    try:
        return get_image_png_base64(files.read_bytes(image), headers)
    except FileNotFoundError:
        pass
    # Out of ideas. Just raise an error
    raise ValueError(f"Could not convert image to PNG: {image}")


async def get_image_png_base64_async(image: ImageLike, headers: Optional[dict] = None) -> str:
    if result := _get_image_png_base64_no_io(image):
        return result
    if (lower := image.lower()).startswith("http://") or lower.startswith("https://"):
        r = await request_async(HttpRequest("get", image, headers=headers, decode=False))
        if r.status_code == 200:
            return await get_image_png_base64_async(r.content)
        raise ValueError(f"Could not download image: {image}")
    try:
        return await get_image_png_base64_async(await files.read_bytes_async(image))
    except FileNotFoundError:
        pass
    raise ValueError(f"Could not convert image to PNG: {image}")


def get_parent_id_or_png_base64(parent: ParentLike, headers: Optional[dict]) -> Union[str, bytes]:
    if isinstance(parent, (Prompt, Generation, WrappedGeneration)):
        return parent.id
    if isinstance(parent, str) and parent.startswith("generation-") or parent.startswith("prompt-"):
        return parent
    return get_image_png_base64(parent, headers)


async def get_parent_id_or_png_base64_async(parent: ParentLike, headers: Optional[dict]) -> Union[str, bytes]:
    if isinstance(parent, (Prompt, Generation, WrappedGeneration)):
        return parent.id
    if isinstance(parent, str) and parent.startswith("generation-") or parent.startswith("prompt-"):
        return parent
    return await get_image_png_base64_async(parent, headers)


class WrappedUserFlag(WrappedResponse):
    wrapped: UserFlag

    def __init__(self, user_flag: UserFlag, dalle: 'Dalle'):
        super().__init__(user_flag, dalle)

    @property
    def id(self) -> str:
        return self.wrapped.id

    @property
    def created(self) -> int:
        return self.wrapped.created

    @property
    def generation_id(self) -> str:
        return self.wrapped.generation_id

    @property
    def description(self) -> str:
        return self.wrapped.description


class WrappedBillingInfo(WrappedResponse):
    wrapped: BillingInfo

    def __init__(self, billing_info: BillingInfo, dalle: 'Dalle'):
        super().__init__(billing_info, dalle)

    @property
    def aggregate_credits(self) -> int:
        return self.wrapped.aggregate_credits

    @property
    def next_grant_ts(self) -> int:
        return self.wrapped.next_grant_ts

    @property
    def breakdown(self) -> Breakdown:
        return self.wrapped.breakdown


class WrappedLogin(WrappedResponse):
    wrapped: Login

    def __init__(self, login: Login, dalle: 'Dalle'):
        super().__init__(login, dalle)

    @property
    def user(self) -> User:
        return self.wrapped.user

    @property
    def invites(self) -> List[Any]:
        return self.wrapped.invites

    @property
    def features(self) -> Features:
        return self.wrapped.features
