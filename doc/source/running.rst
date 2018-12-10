=================
Running syntribos
=================

By default, syntribos looks in the syntribos home directory (the directory
specified when running the ``syntribos init`` command on install) for config
files, payloads, and templates. This can all be overridden through command
line options. For a full list of command line options available, run
``syntribos --help`` from the command line.

To run syntribos against all the available tests, specify the
command ``syntribos``, with the configuration file (if needed), without
specifying any test type.

::

    $ syntribos --config-file keystone.conf run

Fuzzy-matching test names
~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to limit syntribos to run a specific test type using
the ``-t`` flag.

::

    $ syntribos --config-file keystone.conf -t SQL run


This will match all tests that contain ``SQL`` in their name. For example:
``SQL_INJECTION_HEADERS``, ``SQL_INJECTION_BODY``, etc.

Specifying a custom root directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you set up the syntribos environment with a custom root (i.e. with
``syntribos --custom_root init``), you can point to it with the
``--custom_root`` configuration option. Syntribos will look for a
``syntribos.conf`` file inside this directory, and will read further
configuration information from there.
