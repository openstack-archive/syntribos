Running Syntribos
=================


To run Syntribos against all the available tests, just specify command
 ```syntribos``` with the configuration file without specifying any
test type.

::

    $ syntribos --config-file keystone.config run

####Fuzzy-matching test names

It is possible to limit Syntribos to run a specific test type using
the ```-t``` flag..

For example,


::

    $ syntribos --config-file keystone.config -t SQL run


This will match all tests that contain the string 'SQL' in their name,
like SQL_INJECTION_HEADERS, SQL_INJECTION_BODY etc.
