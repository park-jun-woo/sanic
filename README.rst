    **This is a** `filefunc <https://github.com/park-jun-woo/filefunc>`_ **-refactored fork of** `sanic <https://github.com/sanic-org/sanic>`_ **.** All 1865 tests pass identically to the original. See `Refactoring Report`_ below.

.. image:: https://raw.githubusercontent.com/sanic-org/sanic-assets/master/png/sanic-framework-logo-400x97.png
    :alt: Sanic | Build fast. Run fast.

Sanic | Build fast. Run fast.
=============================

.. start-badges

.. list-table::
    :widths: 15 85
    :stub-columns: 1

    * - Build
      - | |Tests|
    * - Docs
      - | |UserGuide| |Documentation|
    * - Package
      - | |PyPI| |PyPI version| |Wheel| |Supported implementations| |Code style ruff|
    * - Support
      - | |Forums| |Discord| |Awesome|
    * - Stats
      - | |Monthly Downloads| |Weekly Downloads| |Conda downloads|

.. |UserGuide| image:: https://img.shields.io/badge/user%20guide-sanic-ff0068
   :target: https://sanic.dev/
.. |Forums| image:: https://img.shields.io/badge/forums-community-ff0068.svg
   :target: https://community.sanicframework.org/
.. |Discord| image:: https://img.shields.io/discord/812221182594121728?logo=discord&label=Discord&color=5865F2
   :target: https://discord.gg/FARQzAEMAA
.. |Tests| image:: https://github.com/sanic-org/sanic/actions/workflows/tests.yml/badge.svg?branch=main
   :target: https://github.com/sanic-org/sanic/actions/workflows/tests.yml
.. |Documentation| image:: https://readthedocs.org/projects/sanic/badge/?version=latest
   :target: http://sanic.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/sanic.svg
   :target: https://pypi.python.org/pypi/sanic/
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/sanic.svg
   :target: https://pypi.python.org/pypi/sanic/
.. |Code style ruff| image:: https://img.shields.io/badge/code%20style-ruff-000000.svg
    :target: https://docs.astral.sh/ruff/
.. |Wheel| image:: https://img.shields.io/pypi/wheel/sanic.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/sanic
.. |Supported implementations| image:: https://img.shields.io/pypi/implementation/sanic.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/sanic
.. |Awesome| image:: https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg
    :alt: Awesome Sanic List
    :target: https://github.com/mekicha/awesome-sanic
.. |Monthly Downloads| image:: https://img.shields.io/pypi/dm/sanic.svg
    :alt: Downloads
    :target: https://pepy.tech/project/sanic
.. |Weekly Downloads| image:: https://img.shields.io/pypi/dw/sanic.svg
    :alt: Downloads
    :target: https://pepy.tech/project/sanic
.. |Conda downloads| image:: https://img.shields.io/conda/dn/conda-forge/sanic.svg
    :alt: Downloads
    :target: https://anaconda.org/conda-forge/sanic

.. end-badges

Sanic is a **Python 3.10+** web server and web framework that's written to go fast. It allows the usage of the ``async/await`` syntax added in Python 3.5, which makes your code non-blocking and speedy.

Sanic is also ASGI compliant, so you can deploy it with an `alternative ASGI webserver <https://sanicframework.org/en/guide/deployment/running.html#asgi>`_.

`Source code on GitHub <https://github.com/sanic-org/sanic/>`_ | `Help and discussion board <https://community.sanicframework.org/>`_ | `User Guide <https://sanicframework.org>`_ | `Chat on Discord <https://discord.gg/FARQzAEMAA>`_

The project is maintained by the community, for the community. **Contributions are welcome!**

The goal of the project is to provide a simple way to get up and running a highly performant HTTP server that is easy to build, to expand, and ultimately to scale.

Sponsor
-------

Check out `open collective <https://opencollective.com/sanic-org>`_ to learn more about helping to fund Sanic.


Installation
------------

``pip install sanic``

    Sanic makes use of ``uvloop`` and ``ujson`` to help with performance. If you do not want to use those packages, simply add an environmental variable ``SANIC_NO_UVLOOP=true`` or ``SANIC_NO_UJSON=true`` at install time.

    .. code:: shell

       $ export SANIC_NO_UVLOOP=true
       $ export SANIC_NO_UJSON=true
       $ pip install --no-binary :all: sanic


.. note::

  If you are running on a clean install of Fedora 28 or above, please make sure you have the ``redhat-rpm-config`` package installed in case if you want to
  use ``sanic`` with ``ujson`` dependency.


Hello World Example
-------------------

.. code:: python

    from sanic import Sanic
    from sanic.response import json

    app = Sanic("my-hello-world-app")

    @app.route('/')
    async def test(request):
        return json({'hello': 'world'})

Sanic can now be easily run from CLI using ``sanic hello.app``.

.. code::

    [2018-12-30 11:37:41 +0200] [13564] [INFO] Goin' Fast @ http://127.0.0.1:8000
    [2018-12-30 11:37:41 +0200] [13564] [INFO] Starting worker [13564]

And, we can verify it is working: ``curl localhost:8000 -i``

.. code::

    HTTP/1.1 200 OK
    Connection: keep-alive
    Keep-Alive: 5
    Content-Length: 17
    Content-Type: application/json

    {"hello":"world"}

**Now, let's go build something fast!**

Minimum Python version is 3.10.

Documentation
-------------

User Guide, Changelog, and API Documentation can be found at `sanic.dev <https://sanic.dev>`__.


Questions and Discussion
------------------------

`Ask a question or join the conversation <https://community.sanicframework.org/>`__.

Contribution
------------

We are always happy to have new contributions. We have `marked issues good for anyone looking to get started <https://github.com/sanic-org/sanic/issues?q=is%3Aopen+is%3Aissue+label%3Abeginner>`_, and welcome `questions on the forums <https://community.sanicframework.org/>`_. Please take a look at our `Contribution guidelines <https://github.com/sanic-org/sanic/blob/master/CONTRIBUTING.md>`_.


.. _Refactoring Report:

filefunc Refactoring Report
---------------------------

This fork restructures sanic to comply with `filefunc <https://github.com/park-jun-woo/filefunc>`_ code structure rules -- an LLM-native convention that enforces "one file, one concept."

What changed
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Metric
     - Original
     - Refactored
   * - Source files
     - 132
     - 396
   * - Total lines
     - 25,772
     - 28,359
   * - filefunc violations
     - N/A (no codebook)
     - 0
   * - pytest passed
     - 1865
     - 1865
   * - pytest failed
     - 0
     - 0

Rules applied
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Rule
     - Description
     - Action taken
   * - F1
     - One function per file
     - Split multi-function files (e.g. ``errorpages.py`` -> 8 files)
   * - F2
     - One class per file
     - Split multi-class files (e.g. ``exceptions.py`` -> 24 files)
   * - Q1
     - Nesting depth max 2
     - Extracted nested logic into helper methods
   * - Q4
     - Control body PURE max 10 lines
     - Extracted large loop/if bodies into private methods
   * - A1/A3
     - ``# ff:func`` and ``# ff:what`` annotations
     - Added to all 396 files
   * - N4
     - Black formatter compliance
     - Applied ``black`` to all files

Verification
~~~~~~~~~~~~

- **Public API**: All public names identical -- every import path preserved via ``__init__.py`` re-exports
- **Import compatibility**: All original import paths work (``from sanic.exceptions import ...``, etc.)
- **Code loss**: 0 functions/classes removed. ~100 private helpers added (extracted from large methods)
- **Runtime behavior**: Full test suite produces identical results
- **Test suite**: 1865 passed, 9 skipped, 3 xfailed -- identical to original
- **Logic comparison**: File-by-file diff verified -- all extracted methods have identical behavior to original inline code

Performance benchmark
~~~~~~~~~~~~~~~~~~~~~

No measurable performance regression. Tested on the same machine, Python 3.12.

.. list-table::
   :header-rows: 1

   * - Benchmark
     - Original
     - Refactored
     - Diff
   * - ``import sanic``
     - 93.8ms
     - 102.0ms
     - +9% (module loading overhead)
   * - App creation + 3 routes
     - 0.19ms
     - 0.19ms
     - 0%
   * - Route resolution ``/users/<id>``
     - 0.7us
     - 0.7us
     - 0%
   * - JSON response creation
     - 1.3us
     - 1.3us
     - 0%
   * - Header parsing
     - 0.9us
     - 0.9us
     - 0%

The 8.2ms import overhead from loading 396 files instead of 132 is a one-time startup cost (~9%). All runtime operations (routing, response, parsing) show zero performance difference.

Structure
~~~~~~~~~

Original hub files (``exceptions.py``, ``headers.py``, ``config.py``, etc.) are preserved as re-export modules for backward compatibility. Split files follow the naming convention ``class_name.py`` or ``function_name.py`` (snake_case).

Exception classes have ``__module__`` set to ``sanic.exceptions`` to preserve ``repr()`` output across the codebase.
