Syntribos
=========

Syntribos is an Automated API Security Testing Tool utilizing the `Open
CAFE Framework <https://github.com/stackforge/opencafe>`__.

Given a simple configuration file and an example HTTP request, Syntribos
can replace any API URL, URL parameter, HTTP header and request body
field with a given set of strings. This is similar to Burp Proxy's
Intruder sniper attack, but Syntribos iterates through each position
automatically. Syntribos aims to automatically detect common security
defects such as SQL injection, LDAP injection, buffer overflow, etc. In
addition, Syntribos can be used to help identifying new security defects
by fuzzing.

Syntribos has the capability to test any API, but is designed with
`OpenStack <http://http://www.openstack.org/>`__ applications in mind.

Index
-----

.. toctree::
    :maxdepth: 1

    installation
    configuration
    running
    logging
    test.anatomy
    unittests
    contributing


Project information
-------------------

* Free software: `Apache license`_
* `Launchpad project`_
* `Blueprints`_
* `Bugs`_

.. _Apache license: https://github.com/openstack/syntribos/blob/master/LICENSE
.. _Launchpad project: https://launchpad.net/syntribos
.. _Blueprints: https://blueprints.launchpad.net/syntribos
.. _Bugs: https://bugs.launchpad.net/syntribos
