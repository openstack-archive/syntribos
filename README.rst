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

Syntribos is an automated API security testing tool that is maintained by
members of the `OpenStack Security Project <https://wiki.openstack.org/wiki/Security>`__.

Given a simple configuration file and an example HTTP request, syntribos
can replace any API URL, URL parameter, HTTP header and request body
field with a given set of strings. Syntribos iterates through each position
in the request automatically. Syntribos aims to automatically detect common
security defects such as SQL injection, LDAP injection, buffer overflow, etc. In
addition, syntribos can be used to help identify new security defects
by automated fuzzing.

Syntribos has the capability to test any API, but is designed with
`OpenStack <http://http://www.openstack.org/>`__ applications in mind.

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

The idea of `buffer overflow`_ in the context of a web application is to force
an application to handle more data than it can hold in a buffer.
In syntribos a buffer overflow test is attempted by injecting a large
string into the body of an HTTP request.

Command Injection
-----------------

`Command injection`_ attacks are done by injecting arbitrary commands in an
attempt to execute these commands on a remote system. In syntribos this is
achieved by injecting a set of strings that have been proven to be successful
in executing a command injection attacks.

CORS Wildcard
-------------

`CORS wildcard`_ test is used to verify if a web server allows cross-domain
resource sharing from any external URL ( wild carding of
`Access-Control-Allow-Origin` header) rather than a white list of URLs.

Integer Overflow
----------------

`Integer overflow`_ test in syntribos attempts to inject numeric values that
the remote application may fail to represent within in its storage, for example
a 32 bit integer type trying to store a 64 bit number

LDAP Injection
--------------

`LDAP injection`_ is attempted in syntribos by injection of LDAP statements
on to HTTP requests; if an application fails to properly sanitize the
request content, it may be possible to execute arbitrary commands.

SQL Injection
-------------

`SQL injection`_ attacks are one of the most common web application attacks.
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

An `XML external entity`_ attack is an attack that targets the web
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

.. _buffer overflow: https://en.wikipedia.org/wiki/Buffer_overflow
.. _Command injection: https://www.owasp.org/index.php/Command_Injection
.. _CORS wildcard: https://www.owasp.org/index.php/Test_Cross_Origin_Resource_Sharing_(OTG-CLIENT-007)
.. _Integer overflow: https://en.wikipedia.org/wiki/Integer_overflow
.. _LDAP injection: https://www.owasp.org/index.php/LDAP_injection
.. _SQL injection: https://www.owasp.org/index.php/SQL_Injection
.. _XML external entity: https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Processing
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

============
Installation
============

Syntribos can be `installed with
pip <https://pypi.python.org/pypi/pip>`__ from the git repository.

-  Clone the repository and install it using pip

::

   $ git clone https://github.com/openstack/syntribos.git
   $ cd syntribos
   $ pip install . --upgrade

=============
Configuration
=============

This is the basic structure of a syntribos configuration file.
All configuration files should have at least the section
``[syntribos]``. Depending upon what extensions you are using
and what you are testing, you can add other sections as well,
for example, if you are using the built-in identity extension
you would also need the ``[user]`` section. The sections
``[logging]`` and ``[remote]`` are optional.

::

    [syntribos]
    #
    # End point URLs and versions of the services to be tested.
    #
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payload_dir=<location_of_payload_dir>

    [user]
    #
    # User credentials and endpoint URI to get an AUTH_TOKEN
    # This section is only needed if you are using the identity extension.
    #
    endpoint=
    username=<yourusername>
    password=<yourpassword>

    [logging]
    log_dir=<location_to_save_debug_logs>


To test any project, just update the endpoint URI under
``[syntribos]`` to point to the API and also modify the user
credentials if needed. The endpoint URI in the ``[syntribos]``
section  is the one being tested by syntribos and the endpoint URI in
``[user]`` section is just used to get an AUTH_TOKEN.


Testing keystone API
~~~~~~~~~~~~~~~~~~~~

A sample config file is given in :file:`examples/configs/keystone.conf`.
Copy this file to a location of your choice (default file path for
configuration file is:  :file:`~/.syntribos/syntribos.conf`) and update the
necessary fields like user credentials, log, template directory etc.

::

    $ vi examples/configs/keystone.conf



    [syntribos]
    #
    # As keystone is being tested in the example, enter your
    #
    # keystone auth endpoint url.
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payload_dir=<location_of_payload_dir>

    [user]
    #
    # User credentials
    #
    endpoint=http://localhost:5000
    username=<yourusername>
    password=<yourpassword>
    # Optional, only needed if Keystone V3 API is used
    #user_id=<youruserid>
    # Optional, api version if required
    #version=v2.0
    # Optional, for getting scoped tokens
    #user_id=<alt_userid>
    # If user id is not known
    # For V3 API
    #domain_name=<name_of_the_domain>
    #project_name=<name_of_the_project>
    # For Keystone V2 API
    #tenant_name=<name_of_the_project>

    #[alt_user]
    #
    # Optional, Used for cross auth tests (-t AUTH)
    #
    #endpoint=http://localhost:5000
    #username=<alt_username>
    #password=<alt_password>
    # Optional, for getting scoped tokens
    #user_id=<alt_userid>
    # If user id is not known
    # For V3 API
    #domain_name=<name_of_the_domain>
    #project_name=<name_of_the_project>
    # For Keystone V2 API
    #tenant_name=<name_of_the_project>

    [logging]
    #
    # Logger options go here
    #
    log_dir=<location_to_store_log_files>
    # Optional, compresses http_request_content,
    # if you don't want this, set this option to False.
    http_request_compression=True

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

=================
Running syntribos
=================

To run syntribos against all the available tests, just specify the
command :command:`syntribos run` with the configuration file without specifying
any test type.

::

    $ syntribos --config-file keystone.conf run

Fuzzy-matching test names
~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to limit syntribos to run a specific test type using
the ``-t`` flag.

::

    $ syntribos --config-file keystone.conf -t SQL run


This will match all tests that contain ``SQL`` in their name
like SQL_INJECTION_HEADERS, SQL_INJECTION_BODY etc.

Syntribos logging
=================
(**This section will be updated shortly**)

Syntribos takes advantage of the OpenCafe logging facility. Logs are
found in ``.opencafe/logs/`` Logs are then arranged in directories based
on each Syntribos configuration file, and then by date and time. Each
log filename has an easy to follow naming convention.

::

    $ ls .opencafe/logs/keystone.config/2015-08-18_14_44_04.333088/
    cafe.master.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str1_model1.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str1_model2.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str1_model3.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str2_model1.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str2_model2.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str2_model3.log

Each log file includes the request details:

::

    ------------
    REQUEST SENT
    ------------
    request method..: POST
    request url.....: https://yourapiendpoint/v3/domains
    request params..:
    request headers.: {'Content-Length': '46', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Accept': 'application/json', 'User-Agent': 'python-requests/2.7.0 CPython/2.7.9 Darwin/11.4.2', 'Host': 'yourapiendpoint', 'X-Auth-Token': u'9b1ed3d1cc69491ab914dcb6ced00440', 'Content-type': 'application/json'}
    request body....: {"domain": {"description": "Domain description","enabled": "-1","name": u'ce9871c4-a0a1-4fbe-88db-f0729b43172c'}}

    2015-08-18 14:44:12,464: DEBUG: cafe.engine.http.client:

and the response:

::

    -----------------
    RESPONSE RECEIVED
    -----------------
    response status..: <Response [406]>
    response time....: 1.32309699059
    response headers.: {'content-length': '112', 'server': 'nginx', 'connection': 'keep-alive', 'date': 'Tue, 18 Aug 2015 19:44:11 GMT', 'content-type': 'application/json; charset=UTF-8'}
    response body....: {"message": "The server could not comply with the request since it is either malformed or otherwise incorrect."}
    -------------------------------------------------------------------------------
    2015-08-18 14:44:12,465: INFO: root: ========================================================
    2015-08-18 14:44:12,465: INFO: root: Test Case....: test_case
    2015-08-18 14:44:12,465: INFO: root: Created At...: 2015-08-18 14:44:11.139070
    2015-08-18 14:44:12,465: INFO: root: No Test description.
    2015-08-18 14:44:12,465: INFO: root: ========================================================
    2015-08-18 14:44:12,465: WARNING: cafe.engine.models.data_interfaces.ConfigParserDataSource: No section: 'fuzz'.  Using default value '200.0' instead
    2015-08-18 14:44:12,465: DEBUG: root: Validate Length:
            Initial request length: 52
            Initial response length: 112
            Request length: 46
            Response length: 112
            Request difference: -6
            Response difference: 0
            Precent difference: 0.0
            Config percent: 200.0

Note the "Validate Length" section at the end. This is used to help
determine whether the test passed or failed. If the *Percent difference*
exceeds the *Config percent* the test has failed. The *Config percent*
is set in ``syntribos/syntribos/tests/fuzz/config.py``. The *Percent
difference* is calculated in
``syntribos/syntribos/tests/fuzz/base_fuzz.py``. Additional validations,
such as looking for SQL strings or stack traces, can be added to
individual tests.

The Logs also contain a summary of data related to the test results
above:

::

    2016-05-19 16:11:52,079: INFO: root: ========================================================
    2016-05-19 16:11:52,079: INFO: root: Test Case......: run_test
    2016-05-19 16:11:52,080: INFO: root: Result.........: Passed
    2016-05-19 16:11:52,080: INFO: root: Start Time.....: 2016-05-19 16:11:52.078475
    2016-05-19 16:11:52,080: INFO: root: Elapsed Time...: 0:00:00.001370
    2016-05-19 16:11:52,080: INFO: root: ========================================================
    2016-05-19 16:11:52,082: INFO: root: ========================================================
    2016-05-19 16:11:52,082: INFO: root: Fixture........: syntribos.tests.fuzz.sql.domains_get.txt_SQL_INJECTION_HEADERS_sql-injection.txt_str19_model2
    2016-05-19 16:11:52,082: INFO: root: Result.........: Passed
    2016-05-19 16:11:52,082: INFO: root: Start Time.....: 2016-05-19 16:11:51.953432
    2016-05-19 16:11:52,083: INFO: root: Elapsed Time...: 0:00:00.129109
    2016-05-19 16:11:52,083: INFO: root: Total Tests....: 1
    2016-05-19 16:11:52,083: INFO: root: Total Passed...: 1
    2016-05-19 16:11:52,083: INFO: root: Total Failed...: 0
    2016-05-19 16:11:52,083: INFO: root: Total Errored..: 0
    2016-05-19 16:11:52,083: INFO: root: ========================================================

===================
Executing unittests
===================

To execute unittests automatically, navigate to the ``syntribos`` root
directory and install the test requirements.

::

    $ pip install -r test-requirements.txt

Now, run

::

    $ python -m unittest discover tests/unit -p "test_*.py"

If you have configured tox you could also do

::

    $ tox -e py27
    $ tox -e py35

This will run all the unittests and give you a result output
containing the status and coverage details of each test.

=======================
Contributing Guidelines
=======================

1. Follow all the `OpenStack Style Guidelines <http://docs.openstack.org/developer/hacking/>`__
   (e.g. PEP8, Py3 compatibility)
2. All new classes/functions should have appropriate docstrings in
   `RST format <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`__
3. All new code should have appropriate unittests (place them in the
   :file:`tests/unit` folder)

Anyone wanting to contribute to OpenStack must follow
`the OpenStack development workflow <http://docs.openstack.org/infra/manual/developers.html#development-workflow>`__

All changes should be submitted through the code review process in Gerrit
described above. All pull requests on Github will be closed/ignored.

Bugs should be filed on the `syntribos launchpad site <https://budmegs.launchpad.net/syntribos>`__,
and not on Github. All Github issues will be closed/ignored.

Breaking changes, feature requests, and other non prioritized work should
first be submitted as a blueprint `here <https://blueprints.launchpad.net/syntribos>`__
for review.

README.rst is auto generated from docs by running :command:`python readme.py` in the
:file:`syntribos/scripts` directory. So when the README.rst needs to be updated;
modify the corresponding rst file in :file:`syntribos/doc/source` and auto generate
the README.

