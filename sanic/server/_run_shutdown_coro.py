# ff:func feature=server type=handler control=sequence
# ff:what Run a shutdown coroutine handling loop-stopped edge cases for asyncio
def _run_shutdown_coro(loop, coro):
    """Run a shutdown coroutine, handling the case where the loop was stopped.

    When loop.stop() is called during run_forever(), asyncio sets an internal
    flag that causes the first run_until_complete() to fail. For standard
    asyncio, we clear the _stopping flag. For uvloop (which doesn't expose
    this flag), the first attempt may fail but subsequent attempts succeed.
    """
    # Clear asyncio's stopped state if accessible
    if hasattr(loop, "_stopping"):
        loop._stopping = False

    try:
        loop.run_until_complete(coro())
    except (RuntimeError, KeyboardInterrupt):
        # RuntimeError: loop was stopped (uvloop behavior)
        # KeyboardInterrupt: signal arrived during select (asyncio behavior)
        # Try once more - this handles uvloop's behavior where the first
        # run_until_complete after stop() fails but subsequent calls succeed.
        if hasattr(loop, "_stopping"):
            loop._stopping = False
        try:
            loop.run_until_complete(coro())
        except (RuntimeError, KeyboardInterrupt):
            # If it still fails, the loop is truly unusable
            pass
