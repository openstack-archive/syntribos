Running syntribos
=================

To execute a Syntribos test, run ``syntribos`` specifying the configuration
file and the test you want to run:

::

    $ syntribos --config-file keystone.config  -t SQL

To run ``syntribos`` against all available tests, just run ``syntribos``
specifying the configuration file:

::

    $ syntribos --config-file keystone.config
