Configuration
=============

This is the basic structure of a Syntribos configuration file.
All config files should have the section ``[syntribos]`` and a
``[user]`` section, the ``[logging]`` section is optional.

::

    [syntribos]
    #
    # End point URLs and versions of the services to be tested.
    #
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payload_dir=<location_of_payload_dir>

    [user]
    #
    # User credentials and endpoint URI to get an AUTH_TOKEN
    #
    endpoint=
    username=<yourusername>
    password=<yourpassword>

    [logging]
    log_dir=<location_to_save_debug_logs>


To test any project, just update the endpoint URI under
``[syntribos]`` to point to the API and also modify the user
credentials if needed. The endpoint URI in the ``[syntribos]``
section  is the one being tested by Syntribos and the endpoint URI in
``[user]`` section is just used to get an AUTH_TOKEN.


Testing Keystone API
--------------------

A sample config file is given in ``examples/configs/keystone.conf``.
Copy this file to a location of your choice (default file path for
configuration file is:  ``~/.syntribos/syntribos.conf``) and update the
necessary fields like user credentials, log, template directory etc.

::

    $ vi examples/configs/keystone.conf



    [syntribos]
    # As keystone is being tested in the example, enter your
    # keystone auth endpoint url.
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payload_dir=<location_of_payload_dir>

    [user]
    #
    # User credentials
    #
    endpoint=http://localhost:5000
    username=<yourusername>
    password=<yourpassword>
    # Optional, only needed if Keystone V3 API is used
    #user_id=<youruserid>
    # Optional, api version if required.
    #version=v2.0


    #[alt_user]
    #
    # Optional, Used for cross auth tests (-t AUTH)
    #

    endpoint=http://localhost:5000
    #username=<alt_username>
    #password=<alt_password>
    #user_id=<alt_userid>



    [logging]
    #
    # Logger options go here
    #
    log_dir=<location_to_store_log_files>
    # Optional, compresses http_request_content,
    # if you don't want this, set this option to False.
    http_request_compression=True
