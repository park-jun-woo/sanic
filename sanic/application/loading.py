# ff:func feature=cli type=util control=sequence
# ff:what Context manager that shows a terminal loading spinner

from contextlib import contextmanager

from sanic.application.spinner import Spinner


@contextmanager
def loading(message: str = "Loading"):  # noqa
    spinner = Spinner(message)
    spinner.start()
    yield
    spinner.stop()
