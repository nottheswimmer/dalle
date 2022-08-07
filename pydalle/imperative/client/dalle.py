"""
A user-friendly interface for the low-level functional API of pydalle.
"""

from typing import Optional, Union, Iterable

from pydalle.functional.api.response.labs import Generation, Task
from pydalle.functional.types import HttpRequest
from pydalle.imperative.api import labs
from pydalle.imperative.outside.internet import request, request_async
from pydalle.imperative.client.responses import WrappedLogin, WrappedBillingInfo, WrappedUserFlag, WrappedCollection, \
    WrappedGeneration, WrappedImage, WrappedTask, WrappedTaskList, GenerationLike, get_generation_id, TaskLike, \
    get_task_id, ParentLike, get_parent_id_or_png_base64, get_parent_id_or_png_base64_async, ImageLike, \
    get_image_png_base64, get_image_png_base64_async
from pydalle.imperative.client.utils import requires_authentication, requires_authentication_async


class Dalle:
    """
    A user-friendly interface for the low-level functional API of pydalle.
    """

    def __init__(self, username: str, password: str, /, headers: Optional[dict] = None):
        """
        Creates a new Dalle instance.

        :param username: The username to use when logging in.
        :param password: The password to use when logging in.
        :param headers: Optional headers to use when making requests.
        """
        if not username:
            raise ValueError("username must not be empty")
        if not password:
            raise ValueError("password must not be empty")

        self.__username = username
        self.__password = password
        self.__access_token = None
        self.__bearer_token = None

        self.headers = headers
        self.has_authenticated = False

    def refresh_tokens(self) -> None:
        """
        Refreshes the access token and bearer token.
        """
        self.__access_token = labs.get_access_token(username=self.__username, password=self.__password,
                                                    headers=self.headers)
        self.__bearer_token = labs.get_bearer_token_from_access_token(access_token=self.__access_token,
                                                                      headers=self.headers)
        self.has_authenticated = True

    async def refresh_tokens_async(self) -> None:
        """
        Asynchronously refreshes the access token and bearer token.
        """
        self.__access_token = await labs.get_access_token_async(username=self.__username, password=self.__password,
                                                                headers=self.headers)
        self.__bearer_token = await labs.get_bearer_token_from_access_token_async(access_token=self.__access_token,
                                                                                  headers=self.headers)
        self.has_authenticated = True

    @requires_authentication
    def get_tasks(self, limit: Optional[int] = None, from_ts: Optional[int] = None) -> WrappedTaskList:
        """
        Gets a list of tasks.

        :param limit: The maximum number of tasks to return.
        :param from_ts: The timestamp to start from.
        :return: A list of tasks.
        """
        return WrappedTaskList(
            labs.get_tasks(bearer_token=self.__bearer_token, from_ts=from_ts, headers=self.headers, limit=limit),
            self)

    @requires_authentication_async
    async def get_tasks_async(self, limit: Optional[int] = None, from_ts: Optional[int] = None) -> WrappedTaskList:
        """
        Asynchronously a list of tasks.

        :param limit: The maximum number of tasks to return.
        :param from_ts: The timestamp to start from.
        :return: A list of tasks.
        """
        return WrappedTaskList(
            await labs.get_tasks_async(bearer_token=self.__bearer_token, from_ts=from_ts, headers=self.headers,
                                       limit=limit), self)

    @requires_authentication
    def get_task(self, task: TaskLike) -> WrappedTask:
        """
        Gets a task.

        :param task: The task to get (either a task ID or a task object).
        :return: The task.
        """
        return WrappedTask(
            labs.get_task(bearer_token=self.__bearer_token, task_id=get_task_id(task), headers=self.headers), self)

    @requires_authentication_async
    async def get_task_async(self, task: TaskLike) -> WrappedTask:
        """
        Asynchronously gets a task.

        :param task: The task to get (either a task ID or a task object).
        :return: The task.
        """
        return WrappedTask(
            await labs.get_task_async(bearer_token=self.__bearer_token, task_id=get_task_id(task),
                                      headers=self.headers),
            self)

    @requires_authentication
    def get_generation(self, generation: GenerationLike) -> WrappedGeneration:
        """
        Gets a generation.

        :param generation: The generation to get (either a generation ID or a generation object).
        :return: The generation.
        """
        return WrappedGeneration(
            labs.get_generation(bearer_token=self.__bearer_token, generation_id=get_generation_id(generation),
                                headers=self.headers), self)

    @requires_authentication_async
    async def get_generation_async(self, generation: GenerationLike) -> WrappedGeneration:
        """
        Asynchronously gets a generation.

        :param generation: The generation to get (either a generation ID or a generation object).
        :return: The generation.
        """
        return WrappedGeneration(
            await labs.get_generation_async(bearer_token=self.__bearer_token,
                                            generation_id=get_generation_id(generation),
                                            headers=self.headers), self)

    @requires_authentication
    def create_text2im_task(self, caption: str, batch_size: int = 4) -> WrappedTask:
        """
        Creates a text2im task.

        :param caption: The caption to use.
        :param batch_size: The batch size to use.
        :return: The task.
        """
        return WrappedTask(
            labs.create_text2im_task(bearer_token=self.__bearer_token, caption=caption, batch_size=batch_size,
                                     headers=self.headers), self)

    @requires_authentication_async
    async def create_text2im_task_async(self, caption: str, batch_size: int = 4) -> WrappedTask:
        """
        Asynchronously creates a text2im task.

        :param caption: The caption to use.
        :param batch_size: The batch size to use.
        :return: The task.
        """
        return WrappedTask(
            await labs.create_text2im_task_async(bearer_token=self.__bearer_token, caption=caption,
                                                 batch_size=batch_size,
                                                 headers=self.headers), self)

    @requires_authentication
    def text2im(self, caption: str, batch_size: int = 4, wait: bool = True) -> WrappedTask:
        """
        Convenience function to create and wait a text2im task.

        :param caption: The caption to use.
        :param batch_size: The batch size to use.
        :param wait: Whether to wait for the task to finish, default is True.
        :return: The task.
        """
        task = self.create_text2im_task(caption=caption, batch_size=batch_size)
        if wait:
            return task.wait()
        return task

    @requires_authentication_async
    async def text2im_async(self, caption: str, batch_size: int = 4, wait: bool = True) -> WrappedTask:
        """
        Asynchronously creates and waits for a text2im task.

        :param caption: The caption to use.
        :param batch_size: The batch size to use.
        :param wait: Whether to wait for the task to finish, default is True.
        :return: The task.
        """
        task = await self.create_text2im_task_async(caption=caption, batch_size=batch_size)
        if wait:
            return await task.wait_async()
        return task

    @requires_authentication
    def create_variations_task(self, parent: ParentLike, batch_size: int = 3) -> WrappedTask:
        """
        Creates a variations task.

        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :return: The task.
        """
        return WrappedTask(
            labs.create_variations_task(bearer_token=self.__bearer_token,
                                        parent_id_or_image=get_parent_id_or_png_base64(parent, self.headers),
                                        batch_size=batch_size, headers=self.headers), self)

    @requires_authentication_async
    async def create_variations_task_async(self, parent: ParentLike, batch_size: int = 3) -> WrappedTask:
        """
        Asynchronously creates a variations task.

        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :return: The task.
        """
        return WrappedTask(await labs.create_variations_task_async(
            bearer_token=self.__bearer_token,
            parent_id_or_image=await get_parent_id_or_png_base64_async(parent, self.headers),
            batch_size=batch_size, headers=self.headers), self)

    @requires_authentication
    def variations(self, parent: ParentLike, batch_size: int = 3, wait: bool = True) -> WrappedTask:
        """
        Convenience function to create and wait a variations task.

        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :param wait: Whether to wait for the task to finish, default is True.
        :return: The task.
        """
        task = self.create_variations_task(parent=parent, batch_size=batch_size)
        if wait:
            return task.wait()
        return task

    @requires_authentication_async
    async def variations_async(self, parent: ParentLike, batch_size: int = 3, wait: bool = True) -> WrappedTask:
        """
        Asynchronously creates and waits for a variations task.

        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :param wait: Whether to wait for the task to finish, default is True.
        :return: The task.
        """
        task = await self.create_variations_task_async(parent=parent, batch_size=batch_size)
        if wait:
            return await task.wait_async()
        return task

    @requires_authentication
    def create_inpainting_task(self, caption: str, masked_image: ImageLike, parent: Optional[ParentLike] = None,
                               batch_size: int = 3) -> WrappedTask:
        """
        Creates an inpainting task.

        :param caption: The caption to use.
        :param masked_image: The masked image to use.
        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :return: The task.
        """
        return WrappedTask(
            labs.create_inpainting_task(
                bearer_token=self.__bearer_token, caption=caption,
                masked_image=get_image_png_base64(masked_image, headers=self.headers),
                parent_id_or_image=get_parent_id_or_png_base64(parent, self.headers) if parent else None,
                batch_size=batch_size,
                headers=self.headers), self)

    @requires_authentication_async
    async def create_inpainting_task_async(self, caption: str,
                                           masked_image: ImageLike,
                                           parent: Optional[ParentLike] = None,
                                           batch_size: int = 3) -> WrappedTask:
        """
        Asynchronously creates an inpainting task.

        :param caption: The caption to use.
        :param masked_image: The masked image to use.
        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :return: The task.
        """
        return WrappedTask(await labs.create_inpainting_task_async(
            bearer_token=self.__bearer_token, caption=caption,
            masked_image=await get_image_png_base64_async(masked_image, self.headers),
            parent_id_or_image=(await get_parent_id_or_png_base64_async(parent, self.headers)) if parent else None,
            batch_size=batch_size, headers=self.headers), self)

    @requires_authentication
    def inpainting(self, caption: str, masked_image: ImageLike, parent: Optional[ParentLike] = None,
                   batch_size: int = 3, wait: bool = True) -> WrappedTask:
        """
        Convenience function to create and wait an inpainting task.

        :param caption: The caption to use.
        :param masked_image: The masked image to use.
        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :param wait: Whether to wait for the task to finish, default is True.
        :return: The task.
        """
        task = self.create_inpainting_task(caption=caption, masked_image=masked_image, parent=parent,
                                           batch_size=batch_size)
        if wait:
            return task.wait()
        return task

    @requires_authentication_async
    async def inpainting_async(self, caption: str, masked_image: ImageLike, parent: Optional[ParentLike] = None,
                               batch_size: int = 3, wait: bool = True) -> WrappedTask:
        """
        Asynchronously creates and waits for an inpainting task.

        :param caption: The caption to use.
        :param masked_image: The masked image to use.
        :param parent: The parent to use. (Either a prompt, a generation, or an image).
        :param batch_size: The batch size to use.
        :param wait: Whether to wait for the task to finish, default is True.
        :return: The task.
        """
        task = await self.create_inpainting_task_async(caption=caption, masked_image=masked_image, parent=parent,
                                                       batch_size=batch_size)
        if wait:
            return await task.wait_async()
        return task

    @requires_authentication
    def poll_for_task_completion(self, task: TaskLike, interval: float = 1.0, max_attempts: int = 1000) -> WrappedTask:
        """
        Polls for the completion of a task.

        :param task: The task to poll.
        :param interval: The interval to use (in seconds).
        :param max_attempts: The maximum number of attempts.
        """
        if isinstance(task, (WrappedTask, Task)):
            if task.status != "pending":
                return task
        return WrappedTask(
            labs.poll_for_task_completion(bearer_token=self.__bearer_token, task_id=get_task_id(task),
                                          interval=interval,
                                          max_attempts=max_attempts, headers=self.headers), self)

    @requires_authentication_async
    async def poll_for_task_completion_async(self, task: TaskLike, interval: float = 1.0,
                                             max_attempts: int = 1000) -> WrappedTask:
        """
        Asynchronously polls for the completion of a task.

        :param task: The task to poll.
        :param interval: The interval to use (in seconds).
        :param max_attempts: The maximum number of attempts.
        """
        if isinstance(task, (WrappedTask, Task)):
            if task.status != "pending":
                return task
        return WrappedTask(
            await labs.poll_for_task_completion_async(bearer_token=self.__bearer_token, task_id=get_task_id(task),
                                                      interval=interval,
                                                      max_attempts=max_attempts, headers=self.headers), self)

    @requires_authentication
    def download_generation(self, generation: GenerationLike, direct: bool = False) -> WrappedImage:
        """
        Downloads a generation.

        :param generation: The generation to download.
        :param direct: Whether to download the generation using the direct download URL, which does not add a watermark.
            You should only use this if you intend to add the watermark to the image yourself. Unwatermarked images
            should not be shared publicly.
        :return: The image.
        """
        if direct:
            return self.download_generation_direct(generation)
        return WrappedImage(labs.download_generation(bearer_token=self.__bearer_token,
                                                     generation_id=get_generation_id(generation),
                                                     headers=self.headers), self)

    @requires_authentication_async
    async def download_generation_async(self, generation: GenerationLike, direct: bool = False) -> WrappedImage:
        """
        Asynchronously downloads a generation.

        :param generation: The generation to download.
        :param direct: Whether to download the generation using the direct download URL, which does not add a watermark.
            You should only use this if you intend to add the watermark to the image yourself. Unwatermarked images
            should not be shared publicly.
        :return: The image.
        """
        if direct:
            return await self.download_generation_direct_async(generation)
        return WrappedImage(await labs.download_generation_async(bearer_token=self.__bearer_token,
                                                                 generation_id=get_generation_id(generation),
                                                                 headers=self.headers), self)

    @requires_authentication
    def download_generation_direct(self, generation: GenerationLike) -> WrappedImage:
        """
        Downloads a generation using the direct download URL, which does not add a watermark.
        You should only use this if you intend to add the watermark to the image yourself. Unwatermarked images
        should not be shared publicly.

        :param generation: The generation to download.
        :return: The image.
        """
        if isinstance(generation, (WrappedGeneration, Generation)):
            image_path = generation.generation.image_path
        else:
            image_path = labs.get_generation(bearer_token=self.__bearer_token,
                                             generation_id=get_generation_id(generation),
                                             headers=self.headers).generation.image_path
        return WrappedImage(
            request(HttpRequest(method="get", url=image_path, headers=self.headers, decode=False)).content, self,
            filetype="webp")

    @requires_authentication_async
    async def download_generation_direct_async(self, generation: GenerationLike) -> WrappedImage:
        """
        Asynchronously downloads a generation using the direct download URL, which does not add a watermark.

        :param generation: The generation to download.
        :return: The image.
        """
        if isinstance(generation, (WrappedGeneration, Generation)):
            image_path = generation.generation.image_path
        else:
            image_path = (await labs.get_generation_async(bearer_token=self.__bearer_token,
                                                          generation_id=get_generation_id(generation),
                                                          headers=self.headers)).generation.image_path
        return WrappedImage(
            (await request_async(
                HttpRequest(method="get", url=image_path, headers=self.headers, decode=False))).content, self,
            filetype="webp")

    @requires_authentication
    def share_generation(self, generation: GenerationLike) -> WrappedGeneration:
        """
        Shares a generation (i.e. people can then download the generation from the share URL).
        See DALL·E 2's `content policy <https://labs.openai.com/policies/content-policy>`_ to see what is OK to share.

        :param generation: The generation to share.
        :return: The shared generation.
        """
        return WrappedGeneration(
            labs.share_generation(bearer_token=self.__bearer_token, generation_id=get_generation_id(generation),
                                  headers=self.headers), self)

    @requires_authentication_async
    async def share_generation_async(self, generation: GenerationLike) -> WrappedGeneration:
        """
        Asynchronously shares a generation (i.e. people can then download the generation from the share URL).
        See DALL·E 2's `content policy <https://labs.openai.com/policies/content-policy>`_ to see what is OK to share.

        :param generation: The generation to share.
        :return: The shared generation.
        """
        return WrappedGeneration(
            await labs.share_generation_async(bearer_token=self.__bearer_token,
                                              generation_id=get_generation_id(generation),
                                              headers=self.headers), self)

    @requires_authentication
    def save_generations(self, generations: Union[Iterable[GenerationLike], GenerationLike]) -> WrappedCollection:
        """
        Saves one or more generations to your personal collection.

        :param generations: The generation(s) to save.
        :return: The collection saved to.
        """
        try:
            generation_ids = [get_generation_id(generations)]
        except ValueError:
            generation_ids = [get_generation_id(generation) for generation in generations]
        return WrappedCollection(labs.save_generations(bearer_token=self.__bearer_token, generation_ids=generation_ids,
                                                       headers=self.headers), self)

    @requires_authentication_async
    async def save_generations_async(self,
                                     generations: Union[Iterable[GenerationLike], GenerationLike]) -> WrappedCollection:
        """
        Asynchronously saves one or more generations to your personal collection.

        :param generations: The generation(s) to save.
        :return: The collection saved to.
        """
        try:
            generation_ids = [get_generation_id(generations)]
        except ValueError:
            generation_ids = [get_generation_id(generation) for generation in generations]
        return WrappedCollection(
            await labs.save_generations_async(bearer_token=self.__bearer_token, generation_ids=generation_ids,
                                              headers=self.headers), self)

    @requires_authentication
    def flag_generation_sensitive(self, generation: GenerationLike) -> WrappedUserFlag:
        """
        Flags a generation as sensitive.

        :param generation: The generation to flag.
        :return: The user flag.
        """
        return WrappedUserFlag(
            labs.flag_generation_sensitive(bearer_token=self.__bearer_token,
                                           generation_id=get_generation_id(generation),
                                           headers=self.headers), self)

    @requires_authentication_async
    async def flag_generation_sensitive_async(self, generation: GenerationLike) -> WrappedUserFlag:
        """
        Asynchronously flags a generation as sensitive.

        :param generation: The generation to flag.
        :return: The user flag.
        """
        return WrappedUserFlag(
            await labs.flag_generation_sensitive_async(bearer_token=self.__bearer_token,
                                                       generation_id=get_generation_id(generation),
                                                       headers=self.headers), self)

    @requires_authentication
    def flag_generation_unexpected(self, generation: GenerationLike) -> WrappedUserFlag:
        """
        Flags a generation as unexpected.

        :param generation: The generation to flag.
        :return: The user flag.
        """
        return WrappedUserFlag(
            labs.flag_generation_unexpected(bearer_token=self.__bearer_token,
                                            generation_id=get_generation_id(generation),
                                            headers=self.headers), self)

    @requires_authentication_async
    async def flag_generation_unexpected_async(self, generation: GenerationLike) -> WrappedUserFlag:
        """
        Asynchronously flags a generation as unexpected.

        :param generation: The generation to flag.
        :return: The user flag.
        """
        return WrappedUserFlag(
            await labs.flag_generation_unexpected_async(bearer_token=self.__bearer_token,
                                                        generation_id=get_generation_id(generation),
                                                        headers=self.headers), self)

    @requires_authentication
    def get_credit_summary(self) -> WrappedBillingInfo:
        """
        Gets the user's credit summary.

        :return: The user's credit summary.
        """
        return WrappedBillingInfo(labs.get_credit_summary(bearer_token=self.__bearer_token, headers=self.headers), self)

    @requires_authentication_async
    async def get_credit_summary_async(self) -> WrappedBillingInfo:
        """
        Asynchronously gets the user's credit summary.

        :return: The user's credit summary.
        """
        return WrappedBillingInfo(
            await labs.get_credit_summary_async(bearer_token=self.__bearer_token, headers=self.headers), self)

    @requires_authentication
    def get_login_info(self) -> WrappedLogin:
        """
        Gets the user's login information.

        :return: The user's login information.
        """
        return WrappedLogin(labs.get_login_info(access_token=self.__access_token, headers=self.headers), self)

    @requires_authentication_async
    async def get_login_info_async(self) -> WrappedLogin:
        """
        Asynchronously gets the user's login information.

        :return: The user's login information.
        """
        return WrappedLogin(await labs.get_login_info_async(access_token=self.__access_token, headers=self.headers),
                            self)
