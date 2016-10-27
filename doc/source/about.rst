=================================================
Syntribos, An Automated API Security Testing Tool
=================================================

::

                      syntribos
                       xxxxxxx
                  x xxxxxxxxxxxxx x
               x     xxxxxxxxxxx     x
                      xxxxxxxxx
            x          xxxxxxx          x
                        xxxxx
           x             xxx             x
                          x
          xxxxxxxxxxxxxxx   xxxxxxxxxxxxxxx
           xxxxxxxxxxxxx     xxxxxxxxxxxxx
            xxxxxxxxxxx       xxxxxxxxxxx
             xxxxxxxxx         xxxxxxxxx
               xxxxxx           xxxxxx
                 xxx             xxx
                     x         x
                          x
             === Automated API Scanning  ===


.. image:: https://img.shields.io/pypi/v/syntribos.svg
    :target: https://pypi.python.org/pypi/syntribos/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/syntribos.svg
    :target: https://pypi.python.org/pypi/syntribos/
    :alt: Downloads

Syntribos is an open source automated API security testing tool that is
maintained by members of the `OpenStack Security Project <https://wiki.openstack.org/wiki/Security>`__.

Given a simple configuration file and an example HTTP request, syntribos
can replace any API URL, URL parameter, HTTP header and request body
field with a given set of strings. Syntribos iterates through each position
in the request automatically. Syntribos aims to automatically detect common
security defects such as SQL injection, LDAP injection, buffer overflow, etc. In
addition, syntribos can be used to help identify new security defects
by automated fuzzing.

Syntribos has the capability to test any API, but is designed with
`OpenStack <https://www.openstack.org/>`__ applications in mind.

List of Tests
~~~~~~~~~~~~~

Syntribos is shipped with batteries included, which means, with minimal
configuration effort you can initiate automated testing of any API of
your choice. If testing OpenStack API is in your mind, then syntribos
by default will help you in automatically downloading a set of templates
of some of the bigger OpenStack projects like nova, neutron, keystone etc.

A short list of tests that can be run using syntribos is given below:

* Buffer Overflow
* Command Injection
* CORS Wildcard
* Integer Overflow
* LDAP Injection
* SQL Injection
* String Validation
* XML External Entity
* Cross Site Scripting ( XSS )

Buffer Overflow
---------------

The idea of `buffer overflow attacks`_ in the context of a web application
is to force an application to handle more data than it can hold in a buffer.
In syntribos a buffer overflow test is attempted by injecting a large
string into the body of an HTTP request.

Command Injection
-----------------

`Command injection attacks`_ are done by injecting arbitrary commands in an
attempt to execute these commands on a remote system. In syntribos, this is
achieved by injecting a set of strings that have been proven to be successful
in executing a command injection attacks.

CORS Wildcard
-------------

`CORS wildcard test`_ is used to verify if a web server allows cross-domain
resource sharing from any external URL ( wild carding of
`Access-Control-Allow-Origin` header) rather than a white list of URLs.

Integer Overflow
----------------

`Integer overflow test`_ in syntribos attempts to inject numeric values that
the remote application may fail to represent within its storage, for example
a 32 bit integer type trying to store a 64 bit number

LDAP Injection
--------------

Syntribos attempts `LDAP injection attacks`_ by injecting LDAP statements
into HTTP requests; if an application fails to properly sanitize the
request content, it may be possible to execute arbitrary commands.

SQL Injection
-------------

`SQL injection attacks`_ are one of the most common web application attacks.
If the user input is not properly sanitized, it is fairly easy to
execute SQL queries that may result in an attacker reading  sensitive
information or gaining control of the SQL server. In syntribos
an application is tested for SQL injection vulnerabilities by injecting
SQL strings into the HTTP request.

String Validation
-----------------

String validation attacks in syntribos try to exploit the fact that
some string patterns are not sanitized effectively by the input
validator and may cause the application to crash. Examples of characters
that may cause string validation vulnerabilities are special unicode
characters, emojis etc.

XML External Entity
-------------------

`XML external entity attacks`_ are attacks that targets the web
application's XML parser. If an XML parser allows processing of
external entities referenced in an XML document then an attacker
might be able to cause denial of service, leakage of information etc.
Syntribos tries to inject a few malicious strings into an XML body
while sending requests to an application in an attempt to obtain an
appropriate response.

Cross Site Scripting ( XSS )
----------------------------
An XSS_ attack is one where malicious JavaScript is injected into a web
application. Syntribos tries to find potential XSS issues by injecting
string containing "script" and other HTML tags into request fields.

Other than these built-in tests, you can extend syntribos by writing
your own custom tests. To do this, download the source code and look at
the tests in ``syntribos/tests`` directory. The CORS test may be an easy
one to emulate. In the same way, users can add different extensions also
to the tests. To see how extensions can be written please see
``syntribos/extensions`` directory.

.. _buffer overflow attacks: https://en.wikipedia.org/wiki/Buffer_overflow
.. _Command injection attacks: https://www.owasp.org/index.php/Command_Injection
.. _CORS wildcard test: https://www.owasp.org/index.php/Test_Cross_Origin_Resource_Sharing_(OTG-CLIENT-007)
.. _Integer overflow test: https://en.wikipedia.org/wiki/Integer_overflow
.. _LDAP injection attacks: https://www.owasp.org/index.php/LDAP_injection
.. _SQL injection attacks: https://www.owasp.org/index.php/SQL_Injection
.. _XML external entity attacks: https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Processing
.. _XSS: https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)

**Details**

* `Documentation`_
* Free software: `Apache license`_
* `Launchpad project`_
* `Blueprints`_
* `Bugs`_
* `Source code`_

Supported Operating Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Syntribos has been developed primarily in Linux and Mac environments and would
work on most Unix and Linux based Operating Systems. At this point, we are not
supporting Windows, but this may change in the future.

.. _Documentation: http://docs.openstack.org/developer/syntribos/
.. _Apache license: https://github.com/openstack/syntribos/blob/master/LICENSE
.. _Launchpad project: https://launchpad.net/syntribos
.. _Blueprints: https://blueprints.launchpad.net/syntribos
.. _Bugs: https://bugs.launchpad.net/syntribos
.. _Source code: https://github.com/openstack/syntribos
