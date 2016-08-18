Configuration
=============

This is the basic structure of a Syntribos configuration file.
All config files should have a section ```[Syntribos]``` and a
```[user]``` section, ```[logging]``` is optional.

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


Testing the Keystone API

::
.
You can modify the file to add your user credentials, log, template
directory etc.

::

    $ vi examples/configs/keystone.config

::

    [syntribos]
    # As keystone is being tested in the example, enter your
    # keystone auth endpoint url.
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payload_dir=<location_of_payload_dir>
    # Optional, api version if required.
    #version=v2

    [user]
    #
    # User credentials
    #
    endpoint=http://localhost:5000
    username=<yourusername>
    password=<yourpassword>
    # Optional, only needed if Keystone V3 API is used
    #user_id=<youruserid>

    #[alt_user]
    #
    # Used for cross auth tests (-t AUTH_WITH_SOMEONE_ELSE_TOKEN)
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


Another example, to test a keystone v3 API, use a configuration like

::

    [syntribos]
    endpoint=http://localhost:5000
    templates=<location_of_template_dir/file>
    payload_dir=<location_of_payloads data>

    [user]
    endpoint=http://localhost:5000
    username=<username>
    password=<password>
    domain_name=default
    domain_id=default

    [logging]
    log_dir=<location_to_store_log_files>
    http_request_compression=True


To test any other project, just change the endpoint URI under
```[syntribos]``` to point to the API and also modify the user
credentials if needed. The endpoint URI in the ```[syntribos]```
section  is the one being tested by Syntribos and the endpoint URI in
```[user]``` section is just used to get an AUTH_TOKEN.

