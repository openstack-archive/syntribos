=============
Configuration
=============

All configuration files should have a ``[syntribos]`` section.
Add other sections depending on what extensions you are using
and what you are testing. For example, if you are using the
built-in identity extension, you would need the ``[user]``
section. The sections ``[logging]`` and ``[remote]`` are optional.

The basic structure of a syntribos configuration
file is given below::

    [syntribos]
    #
    # End point URLs and versions of the services to be tested.
    #
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payloads=<location_of_payloads_dir>

    [user]
    #
    # User credentials and endpoint URL to get an AUTH_TOKEN
    # This section is only needed if you are using the identity extension.
    #
    endpoint=
    username=<yourusername>
    password=<yourpassword>

    [remote]
    #
    # Optional, to define remote URI and cache_dir explicitly
    #
    templates_uri=<URI to a tar file of set of templates>
    payloads_uri=<URI to a tar file of set of payloads>
    cache_dir=<a local path to save the downloaded files>

    [logging]
    log_dir=<location_to_save_debug_logs>

The endpoint URL specified in the ``[syntribos]`` section is the endpoint URL
tested by syntribos. The endpoint URL in the ``[user]`` section is used to
get an AUTH_TOKEN. To test any project, update the endpoint URL under
``[syntribos]`` to point to the API and also modify the user
credentials if needed.

Downloading templates and payloads remotely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Payload and template files can be downloaded remotely in syntribos.
In the config file under the ``[syntribos]`` section, if the ``templates``
and ``payloads`` options are not set, by default syntribos will
download all the latest payloads and the templates for a few OpenStack
projects.

To specify a URI to download custom templates and payloads
from, use the ``[remotes]`` section in the config file.
Available options under ``[remotes]`` are ``cache_dir``, ``templates_uri``,
``payloads_uri``, and ``enable_cache``. The ``enable_cache`` option is
``True`` by default; set to ``False`` to disable caching of remote
content while syntribos is running. If the ``cache_dir`` set to a path,
syntribos will attempt to use that as a base directory to save downloaded
template and payload files.

The advantage of using these options are that you will be able to get
the latest payloads from the official repository and if you are
using syntribos to test OpenStack projects, then, in most cases you
could directly use the well defined templates available with this option.

This option also helps to easily manage different versions of templates
remotely, without the need to maintain a set of different versions offline.

Testing OpenStack keystone API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A sample config file is given in ``examples/configs/keystone.conf``.
Copy this file to a location of your choice (the default file path for the
configuration file is: ``~/.syntribos/syntribos.conf``) and update the
necessary fields, such as user credentials, log, template directory, etc.

::

    $ vi examples/configs/keystone.conf



    [syntribos]
    #
    # As keystone is being tested in the example, enter your
    #
    # keystone auth endpoint url.
    endpoint=http://localhost:5000
    # Set payload and templates path
    templates=<location_of_templates_dir/file>
    payloads=<location_of_payloads_dir>

    [user]
    #
    # User credentials
    #
    endpoint=http://localhost:5000
    username=<yourusername>
    password=<yourpassword>
    # Optional, only needed if Keystone V3 API is used
    #user_id=<youruserid>
    # Optional, api version if required
    #version=v2.0
    # Optional, for getting scoped tokens
    #user_id=<alt_userid>
    # If user id is not known
    # For V3 API
    #domain_name=<name_of_the_domain>
    #project_name=<name_of_the_project>
    # For Keystone V2 API
    #tenant_name=<name_of_the_project>

    #[alt_user]
    #
    # Optional, Used for cross auth tests (-t AUTH)
    #
    #endpoint=http://localhost:5000
    #username=<alt_username>
    #password=<alt_password>
    # Optional, for getting scoped tokens
    #user_id=<alt_userid>
    # If user id is not known
    # For V3 API
    #domain_name=<name_of_the_domain>
    #project_name=<name_of_the_project>
    # For Keystone V2 API
    #tenant_name=<name_of_the_project>

    [remote]
    #
    # Optional, Used to specify URLs of templates and payloads
    #
    #cache_dir=<a local path to save the downloaded files>
    #templates_uri=https://github.com/your_project/templates.tar
    #payloads_uri=https://github.com/your_project/payloads.tar
    # To disable caching of these remote contents, set the following variable to False
    #enable_caching=True

    [logging]
    #
    # Logger options go here
    #
    log_dir=<location_to_store_log_files>
    # Optional, compresses http_request_content,
    # if you don't want this, set this option to False.
    http_request_compression=True
