import logging
import functools
import time
import asyncio
from typing import Callable, Any, TypeVar, cast

from src.core.config import get_settings

settings = get_settings()

# Configure logger
logger = logging.getLogger(__name__)


T = TypeVar('T')


def retry(
    max_tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_tries: Maximum number of retries.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier e.g. value of 2 will double the delay each retry.
        exceptions: Exceptions to catch and retry on.
        
    Returns:
        Decorated function that will retry on specified exceptions.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            mtries, mdelay = max_tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(
                        f"Function {func.__name__} failed with {e.__class__.__name__}. "
                        f"Retrying in {mdelay:.2f} seconds..."
                    )
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return cast(Callable[..., T], wrapper)
    return decorator


def async_retry(
    max_tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Async retry decorator with exponential backoff.
    
    Args:
        max_tries: Maximum number of retries.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier e.g. value of 2 will double the delay each retry.
        exceptions: Exceptions to catch and retry on.
        
    Returns:
        Decorated function that will retry on specified exceptions.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            mtries, mdelay = max_tries, delay
            while mtries > 1:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(
                        f"Function {func.__name__} failed with {e.__class__.__name__}. "
                        f"Retrying in {mdelay:.2f} seconds..."
                    )
                    await asyncio.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return await func(*args, **kwargs)
        return cast(Callable[..., T], wrapper)
    return decorator 