============================
Syntribos Code Documentation
============================

Configuration
~~~~~~~~~~~~~

This section describes the configuration specified in your configuration file
(second argument to the runner).

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
SignalHolders (:class:`syntribos.signal.SignalHolder`)

.. autoclass:: syntribos.signal.SynSignal
    :members:

.. autoclass:: syntribos.signal.SignalHolder
    :members:
    :special-members: __init__, __contains__

Checks
~~~~~~

.. autofunction:: syntribos.checks.http.check_http_fail

.. autofunction:: syntribos.checks.http.check_http_status_code

Tests
~~~~~

This section describes the components involved with writing your own tests with
syntribos.

All syntribos tests inherit from :class:`syntribos.tests.base.BaseTestCase`,
either directly, or through a subclass like
:class:`syntribos.tests.fuzz.base_fuzz.BaseFuzzTestCase`.

All tests are aggregated in the `syntribos.tests.base.test_table` variable

.. automodule:: syntribos.tests.base
    :members:
    :undoc-members:
    :show-inheritance:

..
    .. automodule:: syntribos.tests.fuzz.base_fuzz
        :members:
        :undoc-members:
        :show-inheritance:

.. automodule:: syntribos.tests.fuzz.config
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

This section describes the components related to generating, fuzzing, and making
HTTP requests.

.. automodule:: syntribos.clients.http.client
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: syntribos.clients.http.models
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: syntribos.clients.http.parser
    :members:
    :undoc-members:
    :show-inheritance:

Extension
~~~~~~~~~

This section describes syntribos' extensions, which are called by the
CALL_EXTERNAL field in the request template.

.. automodule:: syntribos.extensions.identity.models.base
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:
