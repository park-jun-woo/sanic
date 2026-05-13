# ff:func feature=server type=config control=sequence
# ff:what Set the asyncio event loop policy to WindowsSelectorEventLoopPolicy
import asyncio

from sanic.compat import OS_IS_WINDOWS
from sanic.log import error_logger


def try_windows_loop():
    """Try to use the WindowsSelectorEventLoopPolicy instead of the default"""
    if not OS_IS_WINDOWS:
        error_logger.warning(
            "You are trying to use an event loop policy that is not "
            "compatible with your system. You can simply let Sanic handle "
            "selecting the best loop for you. Sanic will now continue to run "
            "using the default event loop."
        )
        return

    if not isinstance(
        asyncio.get_event_loop_policy(), asyncio.WindowsSelectorEventLoopPolicy
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
