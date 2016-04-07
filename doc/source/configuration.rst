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

You can create a directory to store the request templates for the resources
being tested. The templates under the `examples` directory can give you a quick
start.
