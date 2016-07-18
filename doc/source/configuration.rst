Configuration
=============

Modify the configuration files to update your Keystone URL, API endpoint
and user credentials.

::

    $ vi examples/configs/keystone.config

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
    # version=v2

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
    # Config for authorization endpoint, so that the service can
    # obtain a valid token, enter your keystone auth endpoint.
    #

    endpoint=http://localhost:5000
