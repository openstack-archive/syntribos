==================
Syntribos Commands
==================

Below are the set of commands that should be specified while
using syntribos.


- :command:`syntribos run`

  This command runs syntribos with the given config options

  ::

    $ syntribos --config-file keystone.conf -t SQL run

- :command:`syntribos dry-run`


  This command ensures that the template files given for this run parse
  successfully without errors. It then runs a debug test which sends no
  requests of its own.

  Note: if any external calls referenced inside the template file do make
  requests, the parser will still make those requests even for a dry run.

  ::

    $ syntribos --config-file keystone.conf dry_run


- :command:`syntribos list_tests`


  This command will list the names and description of all the tests
  that can be executed by the ```run``` command.

  ::

    $ syntribos --config-file keystone.conf list_tests


All these commands will only work if a configuration file
is specified.
