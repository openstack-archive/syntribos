========
Commands
========

Below are the set of commands that can be specified while
using syntribos.

- **init**

  This command sets up the syntribos environment after installation. It will
  create the necessary folders for templates, payloads, and logs, as well as
  an example configuration file.

  ::

    $ syntribos init

  To learn more about ``syntribos init``, see the installation instructions
  `here <installation.html>`_

- **run**

  This command runs syntribos with the given config options

  ::

    $ syntribos --config-file keystone.conf -t SQL run

- **dry-run**

  This command ensures that the template files given for this run parse
  successfully without errors. It then runs a debug test which sends no
  requests of its own.

  Note: If any external calls referenced inside the template file do make
  requests, the parser will still make those requests even for a dry run.

  ::

    $ syntribos --config-file keystone.conf dry_run

- **list_tests**

  This command will list the names and description of all the tests
  that can be executed by the ``run`` command.

  ::

    $ syntribos --config-file keystone.conf list_tests

- **download**

  This command will download templates and payload files. By default, it will
  download a default set of OpenStack template files (with the --templates
  flag) or our default set of payloads (with the --payloads flag) to your
  syntribos root directory. However, the behavior of this command can be
  configured in the [remote] section of your config file.

  ::

    $ syntribos download --templates

All these commands except init will only work if a configuration file
is specified. If a configuration file is present in the default
path ( ``~/.syntribos/syntribos.conf`` ), then you
do not need to explicitly specify a config file and
can run syntribos using the command ``syntribos run``.
