============================
Syntribos Code Documentation
============================

Configuration
~~~~~~~~~~~~~

This section describes the configuration specified in the second argument to
the runner, your configuration file.

.. automodule:: syntribos.config
    :members:
    :undoc-members:
    :show-inheritance:

..
    .. automodule:: syntribos.arguments
        :members:
        :undoc-members:
        :show-inheritance:
    .. automodule:: syntribos.runner
        :members:
        :undoc-members:
        :show-inheritance:

Signals
~~~~~~~

This section describes Signals (:class:`syntribos.signal.SynSignal`) and
SignalHolders (:class:`syntribos.signal.SignalHolder`).

.. autoclass:: syntribos.signal.SynSignal
    :members:

.. autoclass:: syntribos.signal.SignalHolder
    :members:
    :special-members: __init__, __contains__

Checks
~~~~~~

This section describes the checks, which analyze the HTTP response and
returns a signal if it detects something that it knows about. It's intended
to make it easier to inspect HTTP responses.

.. automodule:: syntribos.checks.content_validity
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.fingerprint
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.header
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.http
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.length
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.ssl
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.stacktrace
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.string
    :members:
    :undoc-members:
.. automodule:: syntribos.checks.time
    :members:
    :undoc-members:

Tests
~~~~~

This section describes the components involved with writing your own tests with
syntribos.

All syntribos tests inherit from :class:`syntribos.tests.base.BaseTestCase`,
either directly, or through a subclass such as
:class:`syntribos.tests.fuzz.base_fuzz.BaseFuzzTestCase`.

All tests are aggregated in the ``syntribos.tests.base.test_table`` variable.

.. automodule:: syntribos.tests.base
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: syntribos.tests.fuzz.datagen
    :members:
    :undoc-members:
    :show-inheritance:

Issues
~~~~~~

This section describes the representation of issues that are uncovered by
syntribos.

.. automodule:: syntribos.issue
    :members:
    :undoc-members:
    :show-inheritance:

Results
~~~~~~~

This section describes the representation of results (collections of issues)
from a given syntribos run.

.. automodule:: syntribos.result
    :members:
    :undoc-members:
    :show-inheritance:

HTTP Requests
~~~~~~~~~~~~~

This section describes the components related to generating, fuzzing, and
making HTTP requests.

.. automodule:: syntribos.clients.http.client
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: syntribos.clients.http.parser
    :members:
    :undoc-members:
    :show-inheritance:

Extensions
~~~~~~~~~~

This section describes syntribos extensions, which are called by the
``CALL_EXTERNAL`` field in the request template.

.. automodule:: syntribos.extensions.identity.models.base
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:
