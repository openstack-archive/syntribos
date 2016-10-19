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

Specifying a custom root directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you set up the syntribos environment with a custom root (i.e. with
``syntribos init --custom_install_root``), you can point to it with the
``--syntribos-custom_root`` configuration option. Syntribos will look for a
``syntribos.conf`` file inside this directory, and will read further
configuration information from there.
