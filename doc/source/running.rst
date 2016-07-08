Running syntribos
=================

To execute a Syntribos test, run ``syntribos`` specifying the configuration
file and template file(s) you want to use.

::

    $ syntribos keystone.config .opencafe/templates/keystone/roles_get.txt

To run ``syntribos`` against all template files, just specify the template
directory:

::

    $ syntribos keystone.config .opencafe/templates/keystone/
