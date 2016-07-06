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

Installation
------------

Syntribos can be `installed with
pip <https://pypi.python.org/pypi/pip>`__ from the git repository.

-  Clone the repository and install it using pip

::

   $ git clone https://github.com/openstack/syntribos.git
   $ cd syntribos
   $ pip install . --upgrade

-  To enable autocomplete for Syntribos, run the command.

::

   $ . scripts/syntribos-completion

-  Create a directory named .opencafe in the user's home directory, or in the case of a python virtualenv, in the virtualenv root folder.

::

   $ cafe-config init

-  Install the http library that gives you the minimum plugins required to use Syntribos.

::

   $ cafe-config plugins install http

Configuration
-------------

Copy the data files from Syntribos data directory to .opencafe/data directory created during "cafe-config init". This directory contains the fuzz string files. Copy the example configuration file to .opencafe/configs directory created during "cafe-config init".

::

    $ cp syntribos/data/* .opencafe/data/
    $ cp syntribos/examples/configs/keystone.config  .opencafe/configs/.

Modify the configuration files to update your keystone URL, API endpoint
and user credentials.

::

    $ vi .opencafe/configs/keystone.config

Example configuration file:

::

    [syntribos]
    #
    # End point URLs and versions of the services to be tested.
    #

    # As keystone is being tested in the example, enter your
    # keystone auth endpoint url.
    endpoint=http://localhost:5000

    # Optional, api version if required.
    # Used for cross auth tests (-t AUTH_WITH_SOMEONE_ELSE_TOKEN)
    #version=v2

    [user]
    #
    # User credentials
    #

    username=<yourusername>
    password=<yourpassword>

    # Optional, if keystone V3 API is not used
    #user_id=<youruserid>

    #[alt_user]
    #
    # Used for cross auth tests (-t AUTH_WITH_SOMEONE_ELSE_TOKEN)
    #

    #username=<alt_username>
    #password=<alt_password>
    #user_id=<alt_userid>

    [auth]
    #
    # Config for authorization enpoint, so that the service can
    # obtain a valid token, enter your keystone auth endpoint.
    #

    endpoint=http://localhost:5000


You can create a templates directory inside .opencafe directory to store the request templates for the resources
being tested. The templates under the `examples` directory can give you a quick
start.

::

    $ mkdir .opencafe/templates
    $ mkdir .opencafe/templates/keystone
    $ cp syntribos/examples/templates/keystone/* .opencafe/templates/keystone

Running Syntribos
-----------------

To execute a Syntribos test, run ``syntribos`` specifying the configuration
file and template file(s) you want to use.

::

    $ syntribos keystone.config .opencafe/templates/keystone/roles_get.txt

To run ``syntribos`` against all template files, just specify the template
directory:

::

    $ syntribos keystone.config .opencafe/templates/keystone/

Syntribos Logging
-----------------

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
----------------------------

**Test Types**

The tests included at release time include LDAP injection, SQL
injection, integer overflow and the generic all\_attacks.

In order to run a specific test, simply use the ``-t, --test-types``
option and provide `syntribos` with a keyword or keywords to match from
the test files located in ``syntribos/tests/fuzz/``.

For SQL injection tests, use:

::

    $ syntribos keystone.config templates/keystone/domains_post.txt -t SQL

For SQL injection tests against the template body only, use:

::

    $ syntribos keystone.config template/keystone/domains_post.txt -t SQL_INJECTION_BODY

For all tests against HTTP headers only, use:

::

    $ syntribos keystone.config template/keystone/domains_post.txt -t HEADERS

**Call External**

Syntribos template files can be supplemented with variable data, or data
retrieved from external sources. This is handled using 'extensions.'

Extensions are found in ``syntribos/syntribos/extensions/`` .

One example packaged with Syntribos enables the tester to obtain an auth
token from keystone/identity. The code is located in
``identity/client.py``

To use this extension, you can add the following to your template file:

::

    X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|

The "user" string indicates the data from the configuration file we
added in ``opencafe/configs/keystone.config``

Another example is found in ``random_data/client.py`` . This returns a
UUID when random but unique data is needed. This can be used in place of
usernames when fuzzing a create user call.

::

    "username": "CALL_EXTERNAL|syntribos.extensions.random_data.client:get_uuid:[]|",

The extension function can return one value or be used as a generator if
you want it to change for each test.

**Action Field**

While Syntribos is designed to test all fields in a request, it can also
ignore specific fields through the use of Action Fields. If you want to
fuzz against a static object ID, use the Action Field indicator as
follows:

::

    "ACTION_FIELD:id": "1a16f348-c8d5-42ec-a474-b1cdf78cf40f",

The ID provided will remain static for every test.

Executing Unittests
-------------------

Navigate to the ``syntribos`` root directory

::

    $ python -m unittest discover syntribos/ -p ut_*.py

.. _Apache license: https://github.com/openstack/syntribos/blob/master/LICENSE
.. _Launchpad project: https://launchpad.net/syntribos
.. _Blueprints: https://blueprints.launchpad.net/syntribos
.. _Bugs: https://bugs.launchpad.net/syntribos
