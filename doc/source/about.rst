=================================================
Syntribos, An Automated API Security Testing Tool
=================================================

Syntribos is an open source automated API security testing tool that is
maintained by members of the `OpenStack Security Project <https://wiki.openstack.org/wiki/Security>`_.

Given a simple configuration file and an example HTTP request, syntribos
can replace any API URL, URL parameter, HTTP header and request body
field with a given set of strings. Syntribos iterates through each position
in the request automatically. Syntribos aims to automatically detect common
security defects such as SQL injection, LDAP injection, buffer overflow, etc.
In addition, syntribos can be used to help identify new security defects
by automated fuzzing.

Syntribos has the capability to test any API, but is designed with
`OpenStack <https://www.openstack.org/>`__ applications in mind.

List of Tests
~~~~~~~~~~~~~

With syntribos, you can initiate automated testing of any API with minimal
configuration effort. Syntribos is ideal for testing the OpenStack API as it
will help you in automatically downloading a set of templates of some of the
bigger OpenStack projects like nova, neutron, keystone, etc.

A short list of tests that can be run using syntribos is given below:

* Buffer Overflow
* Command Injection
* CORS Wildcard
* Integer Overflow
* LDAP Injection
* SQL Injection
* String Validation
* XML External Entity
* Cross Site Scripting (XSS)
* Regex Denial of Service (ReDoS)
* JSON Parser Depth Limit
* User Defined

Buffer Overflow
---------------

`Buffer overflow`_ attacks, in the context of a web application,
force an application to handle more data than it can hold in a buffer.
In syntribos, a buffer overflow test is attempted by injecting a large
string into the body of an HTTP request.

Command Injection
-----------------

`Command injection`_ attacks are done by injecting arbitrary commands in an
attempt to execute these commands on a remote system. In syntribos, this is
achieved by injecting a set of strings that have been proven as successful
executors of injection attacks.

CORS Wildcard
-------------

`CORS wildcard`_ tests are used to verify if a web server allows cross-domain
resource sharing from any external URL (wild carding of
`Access-Control-Allow-Origin` header), rather than a white list of URLs.

Integer Overflow
----------------

`Integer overflow`_ tests in syntribos attempt to inject numeric values that
the remote application may fail to represent within its storage. For example,
injecting a 64 bit number into a 32 bit integer type.

LDAP Injection
--------------

Syntribos attempts `LDAP injection`_ attacks by injecting LDAP statements
into HTTP requests; if an application fails to properly sanitize the
request content, it may be possible to execute arbitrary commands.

SQL Injection
-------------

`SQL injection`_ attacks are one of the most common web application attacks.
If the user input is not properly sanitized, it is fairly easy to
execute SQL queries that may result in an attacker reading sensitive
information or gaining control of the SQL server. In syntribos,
an application is tested for SQL injection vulnerabilities by injecting
SQL strings into the HTTP request.

String Validation
-----------------

Some string patterns are not sanitized effectively by the input validator and
may cause the application to crash. String validation attacks in syntribos
try to exploit this by inputting characters that may cause string validation
vulnerabilities. For example, special unicode characters, emojis, etc.

XML External Entity
-------------------

`XML external entity`_ attacks target the web application's XML parser.
If an XML parser allows processing of external entities referenced in an
XML document then an attacker might be able to cause a denial of service,
or leakage of information, etc. Syntribos tries to inject a few malicious
strings into an XML body while sending requests to an application in an
attempt to obtain an appropriate response.

Cross Site Scripting (XSS)
----------------------------

`XSS`_ attacks inject malicious JavaScript into a web
application. Syntribos tries to find potential XSS issues by injecting
string containing "script" and other HTML tags into request fields.

Regex Denial of Service (ReDoS)
-------------------------------

`ReDoS`_ attacks attempt to produce a denial of service by
providing a regular expression that takes a very long time to evaluate.
This can cause the regex engine to backtrack indefinitely, which can
slow down some parsers or even cause a processing halt. The attack
exploits the fact that most regular expression implementations have
an exponential time worst case complexity.

JSON Parser Depth Limit
-----------------------

There is a possibility that the JSON parser will reach depth limit and crash,
resulting in a successful overflow of the JSON parsers depth limit, leading
to a DoS vulnerability. Syntribos tries to check for this, and raises an issue
if the parser crashes.

User defined Test
-----------------

This test gives users the ability to fuzz using user defined fuzz data and
provides an option to look for failure strings provided by the user. The fuzz
data needs to be provided using the config option :option:`[user_defined]`.

Example::

  [user_defined]
  payload=<payload_file>
  failure_strings=<[list_of_failure_strings] # optional

Other than these built-in tests, you can extend syntribos by writing
your own custom tests. To do this, download the source code and look at
the tests in the ``syntribos/tests`` directory. The CORS test may be an easy
one to emulate. In the same way, you can also add different extensions
to the tests. To see how extensions can be written please see the
``syntribos/extensions`` directory.

.. _buffer overflow: https://en.wikipedia.org/wiki/Buffer_overflow
.. _Command injection: https://www.owasp.org/index.php/Command_Injection
.. _CORS wildcard: https://www.owasp.org/index.php/Test_Cross_Origin_Resource_Sharing_(OTG-CLIENT-007)
.. _Integer overflow: https://en.wikipedia.org/wiki/Integer_overflow
.. _LDAP injection: https://www.owasp.org/index.php/LDAP_injection
.. _SQL injection: https://www.owasp.org/index.php/SQL_Injection
.. _XML external entity: https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Processing
.. _XSS: https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)
.. _ReDoS: https://en.wikipedia.org/wiki/ReDoS

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

.. _Documentation: https://docs.openstack.org/developer/syntribos/
.. _Apache license: https://github.com/openstack/syntribos/blob/master/LICENSE
.. _Launchpad project: https://launchpad.net/syntribos
.. _Blueprints: https://blueprints.launchpad.net/syntribos
.. _Bugs: https://bugs.launchpad.net/syntribos
.. _Source code: https://github.com/openstack/syntribos
