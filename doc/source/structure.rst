=================
Project Structure
=================

- ``data/`` (text files containing data for use by syntribos tests)
- ``doc/source/`` (Sphinx documentation files)
- ``examples/`` (example syntribos request templates, config files)
    - ``configs/`` (example syntribos configs)
    - ``templates/`` (examples request templates)
- ``scripts/`` (helper Python scripts for managing the project)
    - ``readme.py`` (Python file for creating/updating the README.rst)
- ``syntribos/`` (core syntribos code)
    - ``clients/`` (clients for making calls, e.g. HTTP)
        - ``http/`` (clients for making HTTP requests)
    - ``checks/`` (for analyzing an HTTP response and returning a signal if
                   it detects something that it knows about)
    - ``extensions/`` (extensions that can be called in request templates)
        - ``identity/`` (extension for interacting with keystone/Identity)
        - ``random_data/`` (extension for generating random test data)
        - ``cinder/`` (extension for interacting with cinder/Block Storage)
        - ``glance/`` (extension for interacting with glance/Image)
        - ``neutron/`` (extension for interacting with neutron/Network)
        - ``nova/`` (extension for interacting with nova/Compute)
    - ``formatters/`` (output formatters, e.g. JSON, XML/XUnit)
    - ``tests/`` (location of tests that syntribos can run against a target)
        - ``auth/`` (tests related to authentication/authorization)
        - ``fuzz/`` (tests that "fuzz" API requests)
        - ``debug/`` (internal syntribos tests, these will not be included in a
                      normal run of syntribos)
        - ``headers/`` (tests related to insecure HTTP headers)
        - ``transport_layer/`` (tests related to SSL and TLS vulnerabilities)
    - ``utils/`` (utility methods)
- ``tests/unit/`` (unit tests for testing syntribos itself)
