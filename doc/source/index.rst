=========
Syntribos
=========

Syntribos is an automated API security testing tool.

Given a simple configuration file and an example HTTP request, syntribos
can replace any API URL, URL parameter, HTTP header and request body
field with a given set of strings. Syntribos iterates through each position
in the request automatically. Syntribos aims to automatically detect common
security defects such as SQL injection, LDAP injection, buffer overflow, etc. In
addition, syntribos can be used to help identify new security defects
by automated fuzzing.

Syntribos has the capability to test any API, but is designed with
`OpenStack <https://www.openstack.org/>`__ applications in mind.

Index
~~~~~

.. toctree::
    :maxdepth: 1

    about
    installation
    configuration
    commands
    running
    logging
    test-anatomy

For Developers
~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    structure
    contributing
    code-docs
    unittests

Project information
~~~~~~~~~~~~~~~~~~~

* `Documentation`_
* Free software: `Apache license`_
* `Launchpad project`_
* `Blueprints`_
* `Bugs`_
* `Source code`_

.. _Documentation: https://docs.openstack.org/developer/syntribos/
.. _Apache license: https://github.com/openstack/syntribos/blob/master/LICENSE
.. _Launchpad project: https://launchpad.net/syntribos
.. _Blueprints: https://blueprints.launchpad.net/syntribos
.. _Bugs: https://bugs.launchpad.net/syntribos
.. _Source code: https://github.com/openstack/syntribos
