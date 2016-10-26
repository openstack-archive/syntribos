=================
Project Structure
=================

- ``data/`` (textfiles containing data for use by syntribos tests)
- ``doc/source/`` (Sphinx documentation files)
- ``examples/`` (example syntribos request templates, config files)
    - ``configs/`` (examples of syntribos configs)
    - ``templates/`` (examples of request templates)
- ``scripts/`` (helper Python scripts for managing the project)
    - ``readme.py`` (Python file for creating/updating the README.rst)
- ``syntribos/`` (core syntribos code)
    - ``clients/`` (clients for making calls, e.g. HTTP)
        - ``http/`` (clients for making HTTP requests)
    - ``checks/`` (for analyzing HTTP response and returning a signal if it detects
                   something that it knows about)
    - ``extensions/`` (extensions that can be called in request templates)
        - ``identity/`` (extension for interacting with Keystone/identity)
        - ``random_data/`` (extension for generating random test data)
        - ``cinder/`` (extension for interacting with Cinder/block storage)
        - ``glance/`` (extension for interacting with Glance/image)
        - ``neutron/`` (extension for interacting with Neutron/network)
        - ``nova/`` (extension for interacting with Nova/compute)
    - ``formatters/`` (output formatters, e.g. JSON, XML/XUnit)
    - ``tests/`` (location of tests that syntribos can run against a target)
        - ``auth/`` (tests related to authentication/authorization)
        - ``fuzz/`` (tests that "fuzz" API requests)
        - ``debug/`` (internal syntribos tests, these will not be included in a
                      normal run of syntribos)
        - ``headers/`` (tests related to insecure HTTP headers)
        - ``transport_layer/`` (tests related to SSL and TLS vulnerabilities)
    - ``utils/`` (utility methods)
- ``tests/unit/`` (unittests for testing syntribos itself)
