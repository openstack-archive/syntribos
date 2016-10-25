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

Syntribos generates results log and debug logs. Result logs are the representation of results
(collection of issues) from a given syntribos run.

Results Log
____________

The result format has the keys "failures" (for tests that failed, indicating a possible security
vulnerability) and "errors" (for tests that encountered some kind of unhandled exception, such
as a connection error).

An example failure object is seen below:

::

    {
       "defect_type": "xss_strings",
       "description": "The string(s): '[\"<STYLE>@import'http://xss.rocks/xss.css';</STYLE>\"]',
       known to be commonly returned after a successful XSS attack, have been found in the
       response. This could indicate a vulnerability to XSS attacks.",
       "failure_id": 33,
       "instances": [
          {
            "confidence": "LOW",
            "param": {
              "location": "data",
              "method": "POST",
              "type": null,
              "variables": [
                "type",
                "details/name",
              ]
          },
          "severity": "LOW",
          "signals": {
             "diff_signals": [
               "LENGTH_DIFF_OVER"
             ],
             "init_signals": [
               "HTTP_CONTENT_TYPE_JSON",
               "HTTP_STATUS_CODE_2XX_201"
             ],
             "test_signals": [
               "FAILURE_KEYS_PRESENT",
               "HTTP_CONTENT_TYPE_JSON",
               "HTTP_STATUS_CODE_2XX_201",
             ]
          },
          "strings": [
            "<STYLE>@import'http://xss.rocks/xss.css';</STYLE>"
             ]
          }
       ],
       "url": "127.0.0.1/test"
    }


Errors take the form:

:: 

    ERROR:
    {
      "error": "Traceback (most recent call last):\n  File \"/Users/test/syntribos/tests/fuzz/base_fuzz.py\",
       line 58, in tearDownClass\n    super(BaseFuzzTestCase, cls).tearDownClass()\n
       File \"/Users/test/syntribos/tests/base.py\", line 166, in tearDownClass\n
       raise sig.data[\"exception\"]\nReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8080):
       Read timed out. (read timeout=10)\n",
       "test": "tearDownClass (syntribos.tests.fuzz.sql.image_data_image_data_get.template_SQL_INJECTION_HEADERS_sql-injection.txt_str21_model1)"
    }


Debug Logs
__________

Debug logs include details about HTTP requests and responses, and any debug information like errors
and warnings across the project. They are found in ``.syntribos/logs/``.
Debug logs are arranged in directories based on date and time, and then
in files according to the templates.

::

    $ ls .syntribos/logs/
    2016-09-15_11:06:37.198412 2016-09-16_10:11:37.834892 2016-09-16_13:31:36.362584
    2016-09-15_11:34:33.271606 2016-09-16_10:38:55.820827 2016-09-16_13:36:43.151048
    2016-09-15_11:41:53.859970 2016-09-16_10:39:50.501820 2016-09-16_13:40:23.203920
    2016-09-15_17:50:54.787628 2016-09-16_10:43:36.158882 2016-09-21_14:07:33.293527
    2016-09-16_10:00:49.615684 2016-09-16_13:30:51.624665 2016-09-21_14:08:26.682639

::

    $ ls .syntribos/logs/2016-09-16_13:31:36.362584
    API_Versions::list_versions_template.log
    API_Versions::show_api_details_template.log
    availability_zones::get_availablilty_zone_detail_template.log
    availability_zones::get_availablilty_zone_template.log
    cells::delete_os_cells_template.log
    cells::get_os_cells_capacities_template.log
    cells::get_os_cells_data_template.log

Each log file includes some essential debugging information like the string representation
of the request object, signals and checks used for tests.

The request:

::

    ------------
    REQUEST SENT
    ------------
    request method.......: PUT
    request url..........: http://127.0.0.1/api
    request params.......:
    request headers size.: 7
    request headers......: {'Content-Length': '0', 'Accept-Encoding': 'gzip, deflate',
    'Accept': 'application/json',
    'X-Auth-Token': <uuid>, 'Connection': 'keep-alive',
    'User-Agent': 'python-requests/2.11.1', 'content-type': 'application/xml'}
    request body size....: 0
    request body.........: None

The response:

::

    -----------------
    RESPONSE RECEIVED
    -----------------
    response status..: <Response [415]>
    response headers.: {'Content-Length': '70',
    'X-Compute-Request-Id': <random id>,
    'Vary': 'OpenStack-API-Version, X-OpenStack-Nova-API-Version',
    'Openstack-Api-Version': 'compute 2.1', 'Connection': 'close',
    'X-Openstack-Nova-Api-Version': '2.1', 'Date': 'Fri, 16 Sep 2016 14:15:27 GMT',
    'Content-Type': 'application/json; charset=UTF-8'}
    response time....: 0.036277
    response size....: 70
    response body....: {"badMediaType": {"message": "Unsupported Content-Type", "code": 415}}
    -------------------------------------------------------------------------------
    [2590]  :  XSS_BODY
    (<syntribos.clients.http.client.SynHTTPClient object at 0x102c65f10>, 'PUT',
    'http://127.0.0.1/api')
    {'headers': {'Accept': 'application/json', 'X-Auth-Token': <uuid> },
    'params': {}, 'sanitize': False, 'data': '', 'requestslib_kwargs': {'timeout': 10}}
    Starting new HTTP connection (1): 127.0.0.1
    "PUT http://127.0.0.1/api HTTP/1.1" 501 93

And the signals captured:

::

    Signals: ['HTTP_STATUS_CODE_4XX_400', 'HTTP_CONTENT_TYPE_JSON']
    Checks used: ['HTTP_STATUS_CODE', 'HTTP_CONTENT_TYPE']

Debug logs are sanitized to prevent storing secrets to log files.
Passwords and other sensitive information are masked with astericks using a slightly modified
version of `oslo_utils.strutils.mask_password <http://docs.openstack.org/developer/oslo.utils/api/strutils.html#oslo_utils.strutils.mask_password_>`

Debug logs also includes body compression, wherein long fuzz strings are compressed before being
written to the logs. The threshold to start data compression is set at 512 characters.
Compression can be turned off by setting the http_request_compression to ``False`` under logging
section in the config file.

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

