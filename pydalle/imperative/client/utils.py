from functools import wraps
from pydalle.functional.types import FlowError, T


def requires_authentication(func: T) -> T:
    """
    Decorator to ensure that the Dalle has authenticated before calling the decorated function
    (or, if it has authenticated but the token has expired, it will refresh the tokens then
    try again).
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # If we have never authenticated, do so now
        if not self.has_authenticated:
            self.refresh_tokens()
        else:
            # Otherwise, we'll try the request and see if it results in an authentication error
            try:
                return func(self, *args, **kwargs)
            except FlowError as e:
                if e.response.status_code == 401:
                    try:
                        if e.response.json()['error']['code'] == "invalid_api_key":
                            # If it does, refresh the tokens and fall through to the last attempt
                            self.refresh_tokens()
                    except Exception:
                        # If it has some other 401 error, reraise it
                        raise e
                else:
                    # If it's not a 401, reraise it
                    raise e
        # If we've gotten here, we should definitely be authenticated
        return func(self, *args, **kwargs)

    return wrapper


def requires_authentication_async(func: T) -> T:
    """
    Async version of the :func:`requires_authentication` decorator.
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.has_authenticated:
            await self.refresh_tokens_async()
        else:
            try:
                return await func(self, *args, **kwargs)
            except FlowError as e:
                if e.response.status_code == 401:
                    try:
                        if e.response.json()['error']['code'] == "invalid_api_key":
                            await self.refresh_tokens_async()
                    except Exception:
                        raise e
                else:
                    raise e
        return await func(self, *args, **kwargs)

    return wrapper
