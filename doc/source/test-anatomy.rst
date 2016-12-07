=============================
Anatomy of a request template
=============================

This section will give you a brief idea on writing templates
and on how to run specific tests. Templates are input files which has
raw http requests and may also be supplemented with variable
data using extensions.

Syntribos template files are ordinary text files containing raw http
requests.

Using external functions in templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These template files can also be supplemented with variable
data, or data retrieved from external sources. This is handled
using 'extensions.'

Extensions are found in ``syntribos/extensions/`` .

Calls to extensions are made in this form:

::

    CALL_EXTERNAL|{extension dot path}:{function}:{arguments}

One example packaged with syntribos enables the tester to obtain an auth
token from keystone. The code is located in ``identity/client.py``

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

Built in functions
------------------

Syntribos comes with a slew of utility functions/extensions, these functions can
be used to dynamically inject data into templates.

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

All these utility functions can be called using:

::

    CALL_EXTERNAL|common_utils.client.{method_name}:{comma separated parameters in square brackets}

For example:

::

    "encoded_url": "CALL_EXTERNAL|common_utils.client:url_encode:['http://localhost:5000']|

There are a few other functions that return random values as well, they are:

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

For example,

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

Running a specific test
~~~~~~~~~~~~~~~~~~~~~~~

As mentioned above, some tests included with syntribos by default
are LDAP injection, SQL injection, integer overflow, command injection,
XML external entity, reflected cross-site scripting,
Cross Origin Resource Sharing (CORS) wildcard and SSL.

In order to run a specific test, simply use the ``-t, --test-types``
option and provide `syntribos` with a keyword or keywords to match from
the test files located in ``syntribos/tests/``.

For SQL injection tests, use:

::

    $ syntribos --config-file keystone.conf -t SQL run

Another example, to run SQL injection tests against the template body only,
use:

::

    $ syntribos --config-file keystone.conf -t SQL_INJECTION_BODY run

For all tests against HTTP headers only, use:

::

    $ syntribos --config-file keystone.conf -t HEADERS run


