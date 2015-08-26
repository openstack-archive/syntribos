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

Syntribos is an automated API security scanner/fuzzer utilizing the [Open CAFE Framework](https://github.com/stackforge/opencafe).

Given a simple configuration file and an example HTTP request, Syntribos can replace any API URL, URL parameter, HTTP header and request body field with a given set of strings. This is similar to Burp Proxy's Intruder sniper attack, but Syntribos iterates through each position automatically. Syntribos aims to automatically detect common security defects such as SQL injection, LDAP injection, buffer overflow, etc. In addtion, Syntribos can be used to help identifying new security defects by fuzzing.   

Syntribos has the capability to test any API, but is designed with [OpenStack](http://http://www.openstack.org/) applications in mind. 


Supported Operating Systems
---------------------------
Syntribos has been developed primarily in Linux and Mac environments, however it supports installation and
execution on Windows. But it has not been tested yet. 


Installation
------------

**Syntribos**

Syntribos can be [installed with pip](https://pypi.python.org/pypi/pip) from the git repository.

* Run `pip install git+git://github.com/PATH_TO_REPO/syntribos` so that pip will auto-install all other dependencies.
* To enable autocomplete for Syntribos, run the command `. scripts/syntribos-completion`


Configuration
--------------
Create .opencafe directory. Then, create .opencafe/data and .opencafe/configs directories. Copy the Syntribos data directory to OpenCafe. This directory contains the fuzz string files. Copy the example configuration file to .opencafe/configs directory. 

```
$mkdir .opencafe
$cp syntribos/data/* .opencafe/data/
mkdir .opencafe/configs
$cp syntribos/examples/configs/keystone.config  .opencafe/configs/.
```

Modify the configuration files to update your keystone url, API endpoint  and user credentails. 

```
vi .opencafe/configs/keystone.config
```

Example configuration file:

```
[syntribos]
endpoint=https://YourAPIEndpoint

[user]
username=yourusername
password=yourpassword
user_id=youruserid


[auth]
endpoint=https://yourkeystoneurl
```

Your can create a directory to store the payloads for the resources being tested. The payloads under examples directory can give you quick start. 

```
$ mkdir payloads
$ mkdir payloads/keystone
$ cp syntribos/examples/payloads/keystone/* payloads/keystone/. 
```

Here are some examples for payload files
```
$ vi payloads/keystone/domains_post.txt
```

```
POST /v3/domains HTTP/1.1
Accept: application/json
X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|
Content-type: application/json

{
    "domain": {
        "description": "Domain description",
        "enabled": true,
        "name": "CALL_EXTERNAL|syntribos.extensions.random_data.client:get_uuid:[]|"
    }
}

```

```
$ vi payloads/keystone/domains_patch.txt
```

```
PATCH /v3/domains/c45412aa3cb74824a222c2f051bd62ac HTTP/1.1
Accept: application/json
X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|
Content-type: application/json

{
    "domain": {
        "description": "Domain description",
        "enabled": true,
        "name": "test name"
    }
}

```

Running Syntribos
-------
To execute a Syntribos test, 
run syntribos specifying the configuration file and payload file(s) you want to use.
```
$ syntribos keystone.config payloads/keystone/domains_post.txt
```
To run syntribos against all payload files, just specify the payload directory:
```
$ syntribos keystone.config payloads/keystone/
```

Basic Syntribos Test Anatomy
-------------------------------

**Test Types**

The tests included at release time include LDAP injection, SQL injection, integer overflow and the generic all_attacks.


In order to run a specific test, simply use the `-t, --test-types` option and provide syntribos with a keyword or keywords to match from the test files located in `syntribos/tests/fuzz/` .

For SQL injection tests, use:
```
$ syntribos keystone.config payloads/keystone/domains_post.txt -t SQL
```
For SQL injection tests against the payload body only, use:
```
$ syntribos keystone.config payloads/keystone/domains_post.txt -t SQL_INJECTION_BODY
```
For all tests against HTTP headers only, use:
```
$ syntribos keystone.config payloads/keystone/domains_post.txt -t HEADERS
```

**Call External**

Syntribos payload files can be supplemented with variable data, or data retrieved from external sources. This is handled using 'extensions.'

Extensions are found in `syntribos/syntribos/extensions/` . 

One example packaged with Syntribos enables the tester to obtain an auth token from keystone/identity. The code is located in `identity/client.py`

To make use of this extension, add the following to the header of your payload file:
```
X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|
```
The "user" string indicates the data from the configuration file we added in `opencafe/configs/keystone.config`


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
