Configuration
=============

Copy the data files from Syntribos data directory to .opencafe/data directory created during "cafe-config init". This directory contains the fuzz string files. Copy the example configuration file to .opencafe/configs directory created during "cafe-config init".

::

    $ cp data/* .opencafe/data/
    $ cp examples/configs/keystone.config  .opencafe/configs/.

Modify the configuration files to update your keystone URL, API endpoint
and user credentials.

::

    $ vi .opencafe/configs/keystone.config

Example configuration file:

::

    [syntribos]
    endpoint=<yourapiendpoint>

    [user]
    username=<yourusername>
    password=<yourpassword>
    user_id=<youruserid>


    [auth]
    endpoint=<yourkeystoneurl>

Your can create a directory to store the payloads for the resources
being tested. The payloads under examples directory can give you quick
start.

::

    $ mkdir payloads
    $ mkdir payloads/keystone
    $ cp examples/payloads/keystone/* payloads/keystone/.

Here are some examples for payload files

::

    $ vi payloads/keystone/domains_post.txt

::

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

::

    $ vi payloads/keystone/domains_patch.txt

::

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

::

    $ vi payloads/keystone/domains_get.txt

::

    GET /v3/domains/{c45412aa3cb74824a222c2f051bd62ac} HTTP/1.1
    Accept: application/json
    X-Auth-Token: CALL_EXTERNAL|syntribos.extensions.identity.client:get_token_v3:["user"]|
