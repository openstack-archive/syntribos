Basic Syntribos Test Anatomy
============================

**Test Types**

The tests included at release time include LDAP injection, SQL
injection, integer overflow, command injection, XML external entity, and
reflected cross-site scripting.

In order to run a specific test, simply use the ``-t, --test-types``
option and provide `syntribos` with a keyword or keywords to match from
the test files located in ``syntribos/tests/fuzz/``.

For SQL injection tests, use:

::

    $ syntribos keystone.config templates/keystone/domains_post.txt -t SQL

For SQL injection tests against the template body only, use:

::

    $ syntribos keystone.config templates/keystone/domains_post.txt -t SQL_INJECTION_BODY

For all tests against HTTP headers only, use:

::

    $ syntribos keystone.config templates/keystone/domains_post.txt -t HEADERS

**Call External**

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
added in ``examples/configs/keystone.config``

Another example is found in ``random_data/client.py`` . This returns a
UUID when random but unique data is needed. This can be used in place of
usernames when fuzzing a create user call.

::

    "username": "CALL_EXTERNAL|syntribos.extensions.random_data.client:get_uuid:[]|"

The extension function can return one value or be used as a generator if
you want it to change for each test.

**Action Field**

While Syntribos is designed to test all fields in a request, it can also
ignore specific fields through the use of Action Fields. If you want to
fuzz against a static object ID, use the Action Field indicator as
follows:

::

    "ACTION_FIELD:id": "1a16f348-c8d5-42ec-a474-b1cdf78cf40f"

The ID provided will remain static for every test.
