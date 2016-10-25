=================
Running syntribos
=================

To run syntribos against all the available tests, just specify the
command ``syntribos`` with the configuration file without
specifying any test type.

::

    $ syntribos --config-file keystone.conf run

Fuzzy-matching test names
~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to limit syntribos to run a specific test type using
the ``-t`` flag.

::

    $ syntribos --config-file keystone.conf -t SQL run


This will match all tests that contain ``SQL`` in their name
like SQL_INJECTION_HEADERS, SQL_INJECTION_BODY etc.
