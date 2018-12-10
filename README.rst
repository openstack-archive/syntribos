
========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/syntribos.svg
    :target: http://governance.openstack.org/reference/tags/index.html


.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
    :target: http://docs.openstack.org/developer/syntribos/

.. image:: http://img.shields.io/pypi/v/syntribos.svg
    :target: http://pypi.python.org/pypi/syntribos/

.. image:: http://img.shields.io/pypi/pyversions/syntribos.svg
        :target: http://pypi.python.org/pypi/syntribos/

.. image:: http://img.shields.io/pypi/wheel/syntribos.svg
        :target: http://pypi.python.org/pypi/syntribos/

.. image:: http://img.shields.io/irc/%23openstack-security.png
        :target: http://webchat.freenode.net/?channels=openstack-security


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
data needs to be provided using the config option `[user_defined]`.

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

============
Installation
============

Syntribos can be installed directly from `pypi with pip <https://pypi.python.org/pypi/pip>`__.

::

   pip install syntribos

For the latest changes, install syntribos from `source <https://www.github.com/openstack/syntribos.git>`__
with `pip <https://pypi.python.org/pypi/pip>`__.

Clone the repository::

   $ git clone https://github.com/openstack/syntribos.git

Change directory into the repository clone and install with pip::

   $ cd syntribos
   $ pip install .

======================================
Initializing the syntribos Environment
======================================

Once syntribos is installed, you must initialize the syntribos environment.
This can be done manually, or with the ``init`` command.

::

    $ syntribos init

.. Note::
    By default, ``syntribos init`` fetches a set of default payload files
    from a `remote repository <https://github.com/openstack/syntribos-payloads>`_
    maintained by our development team. These payload files are necessary for
    our fuzz tests to run. To disable this behavior, run syntribos with the
    ``--no_downloads`` flag. Payload files can also be fetched by running
    ``syntribos download --payloads`` at any time.

To specify a custom root for syntribos to be installed in,
specify the ``--custom_root`` flag. This will skip
prompts for information from the terminal, which can be handy for
Jenkins jobs and other situations where user input cannot be retrieved.

If you've already run the ``init`` command but want to start over with a fresh
environment, you can specify the ``--force`` flag to overwrite existing files.
The ``--custom_root`` and ``--force`` flags can be combined to
overwrite files in a custom install root.

Note: if you install syntribos to a custom install root, you must supply the
``--custom_root`` flag when running syntribos.

**Example:**

::

    $ syntribos --custom_root /your/custom/path init --force
    $ syntribos --custom_root /your/custom/path run



=============
Configuration
=============

All configuration files should have a ``[syntribos]`` section.
Add other sections depending on what extensions you are using
and what you are testing. For example, if you are using the
built-in identity extension, you would need the ``[user]``
section. The sections ``[logging]`` and ``[remote]`` are optional.

The basic structure of a syntribos configuration
file is given below::

    [syntribos]
    #
    # End point URLs and versions of the services to be tested.
    #
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payloads=<location_of_payloads_dir>

    [user]
    #
    # User credentials and endpoint URL to get an AUTH_TOKEN
    # This section is only needed if you are using the identity extension.
    #
    endpoint=
    username=<yourusername>
    password=<yourpassword>

    [remote]
    #
    # Optional, to define remote URI and cache_dir explicitly
    #
    templates_uri=<URI to a tar file of set of templates>
    payloads_uri=<URI to a tar file of set of payloads>
    cache_dir=<a local path to save the downloaded files>

    [logging]
    log_dir=<location_to_save_debug_logs>

The endpoint URL specified in the ``[syntribos]`` section is the endpoint URL
tested by syntribos. The endpoint URL in the ``[user]`` section is used to
get an AUTH_TOKEN. To test any project, update the endpoint URL under
``[syntribos]`` to point to the API and also modify the user
credentials if needed.

Downloading templates and payloads remotely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Payload and template files can be downloaded remotely in syntribos.
In the config file under the ``[syntribos]`` section, if the ``templates``
and ``payloads`` options are not set, by default syntribos will
download all the latest payloads and the templates for a few OpenStack
projects.

To specify a URI to download custom templates and payloads
from, use the ``[remotes]`` section in the config file.
Available options under ``[remotes]`` are ``cache_dir``, ``templates_uri``,
``payloads_uri``, and ``enable_cache``. The ``enable_cache`` option is
``True`` by default; set to ``False`` to disable caching of remote
content while syntribos is running. If the ``cache_dir`` set to a path,
syntribos will attempt to use that as a base directory to save downloaded
template and payload files.

The advantage of using these options are that you will be able to get
the latest payloads from the official repository and if you are
using syntribos to test OpenStack projects, then, in most cases you
could directly use the well defined templates available with this option.

This option also helps to easily manage different versions of templates
remotely, without the need to maintain a set of different versions offline.

Testing OpenStack keystone API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A sample config file is given in ``examples/configs/keystone.conf``.
Copy this file to a location of your choice (the default file path for the
configuration file is: ``~/.syntribos/syntribos.conf``) and update the
necessary fields, such as user credentials, log, template directory, etc.

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
    payloads=<location_of_payloads_dir>

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

    [remote]
    #
    # Optional, Used to specify URLs of templates and payloads
    #
    #cache_dir=<a local path to save the downloaded files>
    #templates_uri=https://github.com/your_project/templates.tar
    #payloads_uri=https://github.com/your_project/payloads.tar
    # To disable caching of these remote contents, set the following variable to False
    #enable_caching=True

    [logging]
    #
    # Logger options go here
    #
    log_dir=<location_to_store_log_files>
    # Optional, compresses http_request_content,
    # if you don't want this, set this option to False.
    http_request_compression=True

========
Commands
========

Below are the set of commands that can be specified while
using syntribos:

- **init**

  This command sets up the syntribos environment after installation. Running
  this command creates the necessary folders for templates, payloads,
  and logs; as well a sample configuration file.

  ::

    $ syntribos init

  To learn more about ``syntribos init``, see the installation instructions
  `here <installation.html>`_.

- **run**

  This command runs syntribos with the given config options.

  ::

    $ syntribos --config-file keystone.conf -t SQL run

- **dry_run**

  This command ensures that the template files given for this run parse
  successfully and without errors. It then runs a debug test which sends no
  requests of its own.

  ::

    $ syntribos --config-file keystone.conf dry_run

.. Note::
    If any external calls referenced inside the template file do make
    requests, the parser will still make those requests even for a dry run.

- **list_tests**

  This command will list the names of all the tests
  that can be executed by the ``run`` command with their description.

  ::

    $ syntribos --config-file keystone.conf list_tests

- **download**

  This command will download templates and payload files. By default, it will
  download a set of OpenStack template files (with the ``--templates``
  flag), or a set of payloads (with the ``--payloads`` flag) to your
  syntribos root directory. However, the behavior of this command can be
  configured in the ``[remote]`` section of your config file.

  ::

    $ syntribos download --templates

.. Important::
    All these commands, except ``init``, will only work if a configuration file
    is specified. If a configuration file is present in the default
    path ( ``~/.syntribos/syntribos.conf`` ), then you
    do not need to explicitly specify a config file and
    can run syntribos using the command ``syntribos run``.

=================
Running syntribos
=================

By default, syntribos looks in the syntribos home directory (the directory
specified when running the ``syntribos init`` command on install) for config
files, payloads, and templates. This can all be overridden through command
line options. For a full list of command line options available, run
``syntribos --help`` from the command line.

To run syntribos against all the available tests, specify the
command ``syntribos``, with the configuration file (if needed), without
specifying any test type.

::

    $ syntribos --config-file keystone.conf run

Fuzzy-matching test names
~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to limit syntribos to run a specific test type using
the ``-t`` flag.

::

    $ syntribos --config-file keystone.conf -t SQL run


This will match all tests that contain ``SQL`` in their name. For example:
``SQL_INJECTION_HEADERS``, ``SQL_INJECTION_BODY``, etc.

Specifying a custom root directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you set up the syntribos environment with a custom root (i.e. with
``syntribos --custom_root init``), you can point to it with the
``--custom_root`` configuration option. Syntribos will look for a
``syntribos.conf`` file inside this directory, and will read further
configuration information from there.

===================
Logging and Results
===================

There are two types of logs generated by syntribos:

#. The results log is a collection of issues generated at the end of a
   syntribos run to represent results.
#. The debug log contains debugging information captured during a particular
   run. Debug logs may include exception messages, warnings, raw
   but sanitized request/response data, and a few more details. A modified
   version of Python logger is used for collecting debug logs in syntribos.

Results Log
~~~~~~~~~~~

The results log is displayed at the end of every syntribos run, it can be
written to a file by using the ``-o`` flag on the command line.

The results log includes failures and errors. The ``"failures"`` key represents
tests that have failed, indicating a possible security vulnerability. The
``"errors"`` key gives us information on any unhandled exceptions, such as
connection errors, encountered on that run.

Example failure object:

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


Error form:

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
~~~~~~~~~~

Debug logs include details about HTTP requests, HTTP responses, and other
debugging information such as errors and warnings across the project. The
path where debug logs are saved by default is ``.syntribos/logs/``.
Debug logs are arranged in directories based on the timestamp in these
directories and files are named according to the templates.

For example:

::

    $ ls .syntribos/logs/
    2016-09-15_11:06:37.198412 2016-09-16_10:11:37.834892 2016-09-16_13:31:36.362584
    2016-09-15_11:34:33.271606 2016-09-16_10:38:55.820827 2016-09-16_13:36:43.151048
    2016-09-15_11:41:53.859970 2016-09-16_10:39:50.501820 2016-09-16_13:40:23.203920

::

    $ ls .syntribos/logs/2016-09-16_13:31:36.362584
    API_Versions::list_versions_template.log
    API_Versions::show_api_details_template.log
    availability_zones::get_availability_zone_detail_template.log
    availability_zones::get_availability_zone_template.log
    cells::delete_os_cells_template.log
    cells::get_os_cells_capacities_template.log
    cells::get_os_cells_data_template.log

Each log file includes some essential debugging information such as the string
representation of the request object, signals, and checks used for tests, etc.

Example request::

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

Example response::

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

Example signals captured::

    Signals: ['HTTP_STATUS_CODE_4XX_400', 'HTTP_CONTENT_TYPE_JSON']
    Checks used: ['HTTP_STATUS_CODE', 'HTTP_CONTENT_TYPE']

Debug logs are sanitized to prevent storing secrets to log files.
Passwords and other sensitive information are marked with asterisks using a
slightly modified version of `oslo_utils.strutils.mask_password <https://docs.openstack.org/developer/oslo.utils/api/strutils.html#oslo_utils.strutils.mask_password>`__.

Debug logs also include string compression, wherein long fuzz strings are
compressed before being written to the logs. The threshold to start data
compression is set to 512 characters. Although it is not recommended to turn
off compression, it is possible by setting the variable
``"http_request_compression"``, under the logging section in the config file,
to ``False``.


=============================
Anatomy of a request template
=============================

This section describes how to write templates and how to run specific tests.
Templates are input files which have raw HTTP requests and may be
supplemented with variable data using extensions.

In general, a request template is a marked-up raw HTTP request. It's possible
for you to test your application by using raw HTTP requests as your request
templates, but syntribos allows you to mark-up your request templates for
further functionality.

A request template looks something like this:

::

    POST /users/{user1} HTTP/1.1
    Content-Type: application/json
    X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.vAPI.client:get_token:[]|

    {"newpassword": "qwerty123"}

For fuzz tests, syntribos will automatically detect URL parameters, headers,
and body content as fields to fuzz. It will not automatically detect URL path
elements as fuzz fields, but they can be specified with curly braces ``{}``.

Note: The name of a template file must end with the extension ``.template``
Otherwise, syntribos will skip the file and will not attempt to parse any files
that do not adhere to this naming scheme.

Using external functions in templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extensions can be used to supplement syntribos template files with variable
data, or data retrieved from external sources.

Extensions are found in ``syntribos/extensions/``.

Calls to extensions are made in the form below:

::

    CALL_EXTERNAL|{extension dot path}:{function name}:[arguments]

One example packaged with syntribos enables the tester to obtain an AUTH
token from keystone. The code is located in ``identity/client.py``.

To use this extension, you can add the following to your template file:

::

    X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|

The ``"user"`` string indicates the data from the configuration file we
added in ``examples/configs/keystone.conf``.

Another example is found in ``random_data/client.py``. This returns a
UUID when random, but unique data is needed. The UUID can be used in place of
usernames when fuzzing a create user call.

::

    "username": "CALL_EXTERNAL|syntribos.extensions.random_data.client:get_uuid:[]|"

The extension function can return one value, or be used as a generator if
you want it to change for each test.

Built in functions
------------------

Syntribos comes with a slew of utility functions/extensions, these functions
can be used to dynamically inject data into templates.

.. list-table:: **Utility Functions**
   :widths: 15 35 40
   :header-rows: 1

   * - Method
     - Parameters
     - Description
   * - hash_it
     - [data, hash_type (optional hash type, default being SHA256)]
     - Returns hashed value of data
   * - hmac_it
     - [data, key, hash_type (optional hash type, default being SHA256)]
     - Returns HMAC based on the has algorithm, data and the key provided
   * - epoch_time
     - [offset (optional integer offset value, default is zero)]
     - Returns the current time minus offset since epoch
   * - utc_datetime
     - []
     - Returns current UTC date time
   * - base64_encode
     - [data]
     - Returns base 64 encoded value of data supplied
   * - url_encode
     - [url]
     - Returns encoded URL

All these utility functions can be called using the following syntax:

::

    CALL_EXTERNAL|common_utils.client.{method_name}:{comma separated parameters in square brackets}

For example:

::

    "encoded_url": "CALL_EXTERNAL|common_utils.client:url_encode:['http://localhost:5000']|

Other functions that return random values can be seen below:

.. list-table:: **Random Functions**
   :widths: 15 35 40
   :header-rows: 1

   * - Method
     - Parameters
     - Description
   * - get_uuid
     - []
     - Returns a random UUID
   * - random_port
     - []
     - Returns random port number between 0 and 65535
   * - random_ip
     - []
     - Returns random ipv4 address
   * - random_mac
     - []
     - Returns random mac address
   * - random_integer
     - [beg (optional beginning value, default is 0), end (optional end value)]
     - Returns an integer value between 0 and 1468029570 by default
   * - random_utc_datetime
     - []
     - Returns random UTC datetime

These can be called using:

::

    CALL_EXTERNAL|random_data.client.{method_name}:{comma separated parameters in square brackets}

For example:

::

    "address": "CALL_EXTERNAL|random_data.client:random_ip:[]|"

Action Field
~~~~~~~~~~~~

While syntribos is designed to test all fields in a request, it can also
ignore specific fields through the use of Action Fields. If you want to
fuzz against a static object ID, use the Action Field indicator as
follows:

::

    "ACTION_FIELD:id": "1a16f348-c8d5-42ec-a474-b1cdf78cf40f"

The ID provided will remain static for every test.

Meta Variable File
~~~~~~~~~~~~~~~~~~

Syntribos allows for templates to read in variables from a user-specified
meta variable file. These files contain JSON objects that define variables
to be used in one or more request templates.

The file must be named `meta.json`, and they take the form:
::

    {
        "user_password": {
            "val": 1234
        },
        "user_name": {
            "type": config,
            "val": "user.username"
            "fuzz_types": ["ascii"]
        },
        "user_token": {
            "type": "function",
            "val": "syntribos.extensions.identity:get_scoped_token_v3",
            "args": ["user"],
            "fuzz": false
        }
    }

To reference a meta variable from a request template, reference the variable
name surrounded by `|` (pipe). An example request template with meta
variables is as follows:
::

    POST /user HTTP/1.1
    X-Auth-Token: |user_token|

    {
        "user": {
            "username": "|user_name|",
            "password": "|user_password|"
        }
    }

Note: Meta-variable usage in templates should take the form `|user_name|`, not
`user_|name|` or `|user|_|name|`. This is to avoid ambiguous behavior when the
value is fuzzed.

Meta Variable Attributes
------------------------
* val - All meta variable objects must define a value, which can be of any json
  DataType. Unlike the other attributes, this attribute is not optional.
* type - Defining a type instructs syntribos to interpret the variable in a
  certain way. Any variables without a type defined will be read in directly
  from the value. The following types are allowed:

  * config - syntribos reads the config value specified by the "val"
    attribute and returns that value.
  * function - syntribos calls the function named in the "val" attribute
    with any arguments given in the optional "args" attribute, and returns the
    value from calling the function. This value is cached, and will be returned
    on subsequent calls.
  * generator - Works the same way as the function type, but its results are
    not cached and the function will be called every time.

* args - A list of function arguments (if any) which can be defined here if the
  variable is a generator or a function
* fuzz - A boolean value that, if set to false, instructs syntribos to
  ignore this variable for any fuzz tests
* fuzz_types - A list of strings which instructs syntribos to only use certain
  fuzz strings when fuzzing this variable. More than one fuzz type can be
  defined. The following fuzz types are allowed:

  * ascii - strings that can be encoded as ascii
  * url - strings that contain only url safe characters

* min_length/max_length - An integer that instructs syntribos to only use fuzz
  strings that meet certain length requirements

Inheritence
-----------

Meta variable files inherit based on the directory it's in. That is, if you
have `foo/meta.json` and `foo/bar/meta.json`, templates in `foo/bar/` will take
their meta variable values from `foo/bar/meta.json`, but they can also
reference meta variables that are defined only in `foo/meta.json`. This also
means that templates in `foo/baz/` cannot reference variables defined only in
`foo/bar/meta.json`.

Each directory can have no more than one file named `meta.json`.

Running a specific test
~~~~~~~~~~~~~~~~~~~~~~~

As mentioned above, some tests included with syntribos by default
are: LDAP injection, SQL injection, integer overflow, command injection,
XML external entity, reflected cross-site scripting,
Cross Origin Resource Sharing (CORS), SSL, Regex Denial of Service,
JSON Parser Depth Limit, and User defined.

In order to run a specific test, use the `-t, --test-types`
option and provide ``syntribos`` with a keyword, or keywords, to match from
the test files located in ``syntribos/tests/``.

For SQL injection tests, see below:

::

    $ syntribos --config-file keystone.conf -t SQL run

To run SQL injection tests against the template body only, see below:

::

    $ syntribos --config-file keystone.conf -t SQL_INJECTION_BODY run

For all tests against HTTP headers only, see below:

::

    $ syntribos --config-file keystone.conf -t HEADERS run


============
Unit testing
============

To execute unit tests automatically, navigate to the ``syntribos`` root
directory and install the test requirements.

::

    $ pip install -r test-requirements.txt

Now, run the ``unittest`` as below:

::

    $ python -m unittest discover tests/unit -p "test_*.py"

If you have configured tox you could also run the following:

::

    $ tox -e py27
    $ tox -e py35

This will run all the unit tests and give you a result output
containing the status and coverage details of each test.

=======================
Contributing Guidelines
=======================

Syntribos is an open source project and contributions are always
welcome. If you have any questions, we can be found in the
#openstack-security channel on Freenode IRC.

1. Follow all the `OpenStack Style Guidelines <https://docs.openstack.org/developer/hacking/>`__
   (e.g. PEP8, Py3 compatibility)
2. Follow `secure coding guidelines <https://security.openstack.org/#secure-development-guidelines>`__
3. Ensure all classes/functions have appropriate `docstrings <https://www.python.org/dev/peps/pep-0257/>`__
   in  `RST format <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`__
4. Include appropriate unit tests for all new code(place them in the
   ``tests/unit`` folder)
5. Test any change you make using tox:

  ::

    pip install tox
    tox -e pep8
    tox -e py27
    tox -e py35
    tox -e cover

Anyone wanting to contribute to OpenStack must follow
`the OpenStack development workflow <https://docs.openstack.org/infra/manual/developers.html#development-workflow>`__

Submit all changes through the code review process in Gerrit
described above. All pull requests on Github will be closed/ignored.

File bugs on the `syntribos launchpad site <https://bugs.launchpad.net/syntribos>`__,
and not on Github. All Github issues will be closed/ignored.

Submit blueprints `here <https://blueprints.launchpad.net/syntribos>`__ for all
breaking changes, feature requests, and other unprioritized work.


.. Note:: README.rst is a file that can be generated by running
   ``python readme.py`` from the ``syntribos/scripts`` directory. When the
   README file needs to be updated; modify the corresponding rst file in
   ``syntribos/doc/source`` and have it generate by running the script.

