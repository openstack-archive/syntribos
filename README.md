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
**CloudCafe** (required)

CloudCAFE can be [installed with pip](https://pypi.python.org/pypi/pip) from the git repository after it is cloned to
a local machine.

* First follow the README instructions to install [Open CAFE Core](https://github.com/stackforge/opencafe).
* Clone this repository to your local machine.
* CD to the cloned cloudcafe repository directory.
* Run `pip install . --upgrade` so that pip will auto-install all other dependencies.

**Syntribos**

Syntribos can be [installed with pip](https://pypi.python.org/pypi/pip) from the git repository after it is cloned to
a local machine.

* Clone [Syntribos](https://github.com/rackerlabs/syntribos) to the same local directory as CloudCafe.
* CD to the cloned Syntribos repository directory.
* Run `pip install . --upgrade` so that pip will auto-install all other dependencies.
* To enable autocomplete for Syntribos, run the following command `. scripts/syntribos-completion`


Configuration
--------------
Copy the Syntribos data directory to CloudCafe 

```
$ cp syntribos/data/* .opencafe/data/`
```

Create a configuration file for the API being tested 

```
mkdir .opencafe/configs/API_NAME.config
```

Example configuration file:

```
[syntribos]
endpoint=https://TESTING.API.ENDPOINT.com

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
$ mkdir payload/API_NAME
```

Create a payload file for the resource being tested 
* Note the extension specified. This retrieves the X-Auth-Token using Rackspace Cloud Auth. The [auth] endpoint is specified in the the configuration file above.

```
$ vi payloads/API_NAME/list_users.txt`
```

```
GET /v2.0/users?name=&email= HTTP/1.1
Host: TESTING.API.ENDPOINT.com
Accept: application/json
X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.rax_auth.client:get_token:["user"]|
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
$ syntribosAPI_NAMEE.config payloads/API_NAME/list_users.txt
```

Basic Syntribos Package Anatomy
-------------------------------
Below is a short description of the top level Syntribos Packages.

TBD

Executing Unittests
-------------------
Navigate to the syntribos root directory
```
python -m unittest discover syntribos/ -p ut_*.py
```
