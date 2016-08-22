Syntribos Commands
===================

Below are the set of commands that should be specified while
using Syntribos.


- **run**

  This command runs Syntribos with the given config options

  ::

    $ syntribos --config-file keystone.conf -t SQL run

- **dry_run**


  This command prepares all the test cases that would be executed by
  the ```run``` command based on the configuration options passed to
  Syntribos, but simply prints their details to the screen instead
  of actually running them.

  ::

    $ syntribos --config-file keystone.conf -t SQL dry_run


- **list_tests**


  This command will list the names and description of all the tests
  that can be executed by the ```run``` command.

  ::

    $ syntribos --config-file keystone.conf list_tests


All these commands will only work if a configuration file
is specified.
