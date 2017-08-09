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

In order to run a specific test, use the :option:`-t, --test-types`
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

