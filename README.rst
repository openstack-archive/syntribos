Syntribos, An Automated API Security Testing Tool
=================================================

::

                      Syntribos
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

**Details**

* Free software: `Apache license`_
* `Launchpad project`_
* `Blueprints`_
* `Bugs`_

Supported Operating Systems
---------------------------

Syntribos has been developed primarily in Linux and Mac environments,
however it supports installation and execution on Windows. But it has
not been tested yet.

.. _Apache license: https://github.com/openstack/syntribos/blob/master/LICENSE
.. _Launchpad project: https://launchpad.net/syntribos
.. _Blueprints: https://blueprints.launchpad.net/syntribos
.. _Bugs: https://bugs.launchpad.net/syntribos

Installation
============

Syntribos can be `installed with
pip <https://pypi.python.org/pypi/pip>`__ from the git repository.

-  Clone the repository and install it using pip

::

   $ git clone https://github.com/openstack/syntribos.git
   $ cd syntribos
   $ pip install . --upgrade

Configuration
=============

This is the basic structure of a Syntribos configuration file.
All config files should have the section ``[syntribos]`` and a
``[user]`` section, the ``[logging]`` section is optional.

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
    #
    endpoint=
    username=<yourusername>
    password=<yourpassword>

    [logging]
    log_dir=<location_to_save_debug_logs>


To test any project, just update the endpoint URI under
``[syntribos]`` to point to the API and also modify the user
credentials if needed. The endpoint URI in the ``[syntribos]``
section  is the one being tested by Syntribos and the endpoint URI in
``[user]`` section is just used to get an AUTH_TOKEN.


Testing Keystone API
--------------------


A sample config file is given in ``examples/configs/keystone.conf``.
Copy this file to a location of your choice (default file path for
configuration file is:  ``~/.syntribos/syntribos.conf``) and update the
necessary fields like user credentials, log, template directory etc.

::

    $ vi examples/configs/keystone.conf



    [syntribos]
    # As keystone is being tested in the example, enter your
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
    # Optional, api version if required.
    #version=v2.0


    #[alt_user]
    #
    # Optional, Used for cross auth tests (-t AUTH)
    #

    endpoint=http://localhost:5000
    #username=<alt_username>
    #password=<alt_password>
    #user_id=<alt_userid>



    [logging]
    #
    # Logger options go here
    #
    log_dir=<location_to_store_log_files>
    # Optional, compresses http_request_content,
    # if you don't want this, set this option to False.
    http_request_compression=True

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

Running Syntribos
=================

To run Syntribos against all the available tests, just specify the
command ``syntribos`` with the configuration file without specifying
any test type.

::

    $ syntribos --config-file keystone.config run

Fuzzy-matching test names
--------------------------

It is possible to limit Syntribos to run a specific test type using
the ``-t`` flag..

::

    $ syntribos --config-file keystone.config -t SQL run


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

Basic Syntribos Test Anatomy
============================

Test Types
----------

The tests included at release time include LDAP injection, SQL
injection, integer overflow, command injection, XML external entity,
reflected cross-site scripting, Cross Origin Resource Sharing (CORS)
wildcard and SSL.

In order to run a specific test, simply use the ``-t, --test-types``
option and provide `syntribos` with a keyword or keywords to match from
the test files located in ``syntribos/tests/``.

For SQL injection tests, use:

::

    $ syntribos --config-file keystone.conf -t SQL

Another example, to run SQL injection tests against the template body only, use:

::

    $ syntribos --config-file keystone.conf -t SQL_INJECTION_BODY

For all tests against HTTP headers only, use:

::

    $ syntribos --config-file keystone.conf -t HEADERS


Call External
-------------

Syntribos template files can be supplemented with variable data, or data
retrieved from external sources. This is handled using 'extensions.'

Extensions are found in ``syntribos/extensions/`` .

Calls to extensions are made in this form:

::

    CALL_EXTERNAL|{extension dot path}:{function}:{arguments}

One example packaged with Syntribos enables the tester to obtain an auth
token from keystone/identity. The code is located in
``identity/client.py``

To use this extension, you can add the following to your template file:

::

    X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|

The "user" string indicates the data from the configuration file we
added in ``examples/configs/keystone.conf``

Another example is found in ``random_data/client.py`` . This returns a
UUID when random but unique data is needed. This can be used in place of
usernames when fuzzing a create user call.

::

    "username": "CALL_EXTERNAL|syntribos.extensions.random_data.client:get_uuid:[]|"

The extension function can return one value or be used as a generator if
you want it to change for each test.


Action Field
------------

While Syntribos is designed to test all fields in a request, it can also
ignore specific fields through the use of Action Fields. If you want to
fuzz against a static object ID, use the Action Field indicator as
follows:

::

    "ACTION_FIELD:id": "1a16f348-c8d5-42ec-a474-b1cdf78cf40f"

The ID provided will remain static for every test.

Executing unittests
===================

To execute unittests automatically, navigate to the ``syntribos`` root
directory and install the test requirements.

::
    $ pip install -r test-requirements.txt

Now, run

::

    $ python -m unittest discover tests/unit -p "test_*.py"

Also, if  you have configured tox you could also do

::
    $ tox -e py27

This will run all the unittests and give you a result output
containing the status and coverage details of each test.

Contributing Guidelines
========================

1. Follow all the `OpenStack Style Guidelines <http://docs.openstack.org/developer/hacking/>`__
   (e.g. PEP8, Py3 compatibility)
2. All new classes/functions should have appropriate docstrings in
   `RST format <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`__
3. All new code should have appropriate unittests (place them in the
   ``tests/unit`` folder)

Anyone wanting to contribute to OpenStack must follow
`the OpenStack development workflow <http://docs.openstack.org/infra/manual/developers.html#development-workflow>`__

All changes should be submitted through the code review process in Gerrit
described above. All pull requests on Github will be closed/ignored.

Bugs should be filed on the `Syntribos launchpad site <https://bugs.launchpad.net/syntribos>`__,
and not on Github. All Github issues will be closed/ignored.

Breaking changes, feature requests, and other non prioritized work should
first be submitted as a blueprint `here <https://blueprints.launchpad.net/syntribos>`__
for review.

