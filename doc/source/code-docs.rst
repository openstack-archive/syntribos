Syntribos Code Documentation
============================

Configuration
-------------

This section describes the configuration specified in your configuration file
(second argument to the runner).

.. autoclass:: syntribos.config.MainConfig
    :members:

..
    Arguments
    ---------
    .. autoclass:: syntribos.arguments.SyntribosCLI
        :members:

..
    Runner
    ------
    .. autoclass:: syntribos.runners.Runner
        :members:

Tests
-----

This section describes the components involved with writing your own tests with
Syntribos.

All Syntribos tests inherit from :class:`syntribos.tests.base.BaseTestCase`,
either directly, or through a subclass like
:class:`syntribos.tests.fuzz.base_fuzz.BaseFuzzTestCase`.

All tests are aggregated in the `syntribos.tests.base.test_table` variable

.. autoclass:: syntribos.tests.base.TestType
    :members:

.. autoclass:: syntribos.tests.base.BaseTestCase
    :members:

.. autofunction:: syntribos.tests.base.replace_invalid_characters


..
    .. autoclass:: syntribos.tests.fuzz.base_fuzz.BaseFuzzTestCase
        :members:


Issues
------

This section describes the representation of issues that are uncovered by
Syntribos.

.. autoclass:: syntribos.issue.Issue
    :members:

Results
-------

This section describes the representation of results (collections of issues)
from a given Syntribos run.

.. autoclass:: syntribos.result.IssueTestResult
    :members:

HTTP Requests
-------------

This section describes the components related to generating, fuzzing, and making
HTTP requests.

.. autoclass:: syntribos.clients.http.parser.RequestCreator
    :members:
    :private-members:

.. autoclass:: syntribos.clients.http.models.RequestObject
    :members:

.. autoclass:: syntribos.clients.http.models.RequestHelperMixin
    :members:
    :private-members:
