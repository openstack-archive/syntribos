Running syntribos
=================

To execute a Syntribos test, run ``syntribos`` specifying the configuration
file and payload file(s) you want to use.

::

    $ syntribos keystone.config payloads/keystone/domains_post.txt

To run ``syntribos`` against all payload files, just specify the payload
directory:

::

    $ syntribos keystone.config payloads/keystone/
