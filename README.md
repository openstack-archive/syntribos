Syntribos, An automated API scanner
====================================================

<pre>
----------------------------------------

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
----------------------------------------
</pre>

Syntribos is an automated API scanner/fuzzer utilizing the [Open CAFE Framework](https://github.com/stackforge/opencafe).
Syntribos has the capability to test any API, but is designed with [OpenStack](http://http://www.openstack.org/) applications in mind. 
It is built using the [Open CAFE Core](https://github.com/stackforge/opencafe).


Supported Operating Systems
---------------------------
Syntribos has been developed primarily in Linux and Mac environments, however it supports installation and
execution on Windows.


Installation
------------

**Syntribos**

Syntribos can be [installed with pip](https://pypi.python.org/pypi/pip) from the git repository.

* Run `pip install git+git://github.com/PATH_TO_REPO/syntribos` so that pip will auto-install all other dependencies.
* To enable autocomplete for Syntribos, run the following command `. scripts/syntribos-completion`


Configuration
--------------
Copy the Syntribos data directory to OpenCafe 

```
$ cp syntribos/data/* .opencafe/data/`
```

Create a configuration directory and file for the API being tested 

```
mkdir .opencafe/configs
vi .opencafe/configs/API_NAME.config
```

Example configuration file:

```
[syntribos]
endpoint=https://API.ENDPOINT.TO.BE.TESTED.com

[user]
username=USERNAME
password=PASSWORD

[user2]
username=USERNAME2
password=PASSWORD2

[auth]
endpoint=https://AUTH.API.ENDPOINT.com/v2.0
```

Create a directory to store payloads for API being tested.

Create a directory to store the payloads for the resources being tested. 

```
$ mkdir payloads
$ mkdir payloads/API_NAME
```

Create a payload file for the resource being tested 
```
$ vi payloads/API_NAME/list_users.txt`
```

```
GET /v2.0/users?name=newUser&email=newUser@example.com HTTP/1.1
Host: TESTING.API.ENDPOINT.com
Accept: application/json
Content-type: application/json


```

```
$ vi payloads/API_NAME/create_user.txt
```

```
POST /v2.0/users HTTP/1.1
Host: TESTING.API.ENDPOINT.com
Accept: application/json
X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.rax_auth.client:get_token:["user"]|
Content-type: application/json

{
  "user": {
    "username": "newUser",
    "email": "newUser@example.com",
    "enabled": true
    }
}


```

Running Syntribos
-------
To execute a Syntribos test, 
run syntribos specifying the configuration file and payload file(s) you want to use.
```
$ syntribos API_NAME.config payloads/API_NAME/list_users.txt
```
To run syntribos against all payload files, just specify the payload directory:
```
$ syntribos API_NAME.config payloads/API_NAME/
```

Basic Syntribos Test Anatomy
-------------------------------

**Test Types**

The tests included at release time include LDAP injection, SQL injection, integer overflow and the generic all_attacks.


In order to run a specific test, simply use the `-t, --test-types` option and provide syntribos with a keyword or keywords to match from the test files located in `syntribos/tests/fuzz/`
For SQL injection tests, use:
```
$ syntribos API_NAME.config payloads/API_NAME/list_users.txt SQL
```
For SQL injection tests against the payload body only, use:
```
$ syntribos API_NAME.config payloads/API_NAME/create_user.txt -t SQL_INJECTION_BODY
```
For all tests against HTTP headers only, use:
```
$ syntribos API_NAME.config payloads/API_NAME/list_users.txt -t HEADERS
```

**Call External**

Syntribos payload files can be supplemented with data that can be variable or retrieved from external sources. This is handled using 'extensions.'

Extensions are found in `syntribos/syntribos/extensions/` . 

One example packaged with Syntribos enables the tester to obtain an auth token from keystone/identity. The code is located in `identity/client.py`

To make use of this extension, add the following to the header of your payload file:
```
X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token:["user"]|
```
The "user" string indicates the data from the configuration file we added in `opencafe/configs/API_NAME.config`
In the example API_NAME.config, we have user and user2 available.

Another example is found in `random_data/client.py` . This returns a UUID when random but unique data is needed. This can be used in place of usernames when fuzzing a create user call.
```
"username": "CALL_EXTERNAL|syntribos.extensions.random_data.client:get_uuid:[]|",
```

The extension function can return one value or be used as a generator if you want it to change for each test.

**Action Field**

While Syntribos is designed to test all fields in a request, it can also ignore specific fields through the use of Action Fields.
If you want to fuzz against a static object ID, use th Action Field indicator as follows:
```
"id": "ACTION_FIELD:1a16f348-c8d5-42ec-a474-b1cdf78cf40f",
```
The ID provided will remain static for every test.



Executing Unittests
-------------------
Navigate to the syntribos root directory
```
python -m unittest discover syntribos/ -p ut_*.py
```
