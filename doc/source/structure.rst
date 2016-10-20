=================
Project Structure
=================

- ``data/`` (textfiles containing data for use by syntribos tests)
- ``doc/source/`` (Sphinx documentation files)
- ``examples/`` (example syntribos request templates, config files)
    - ``configs/`` (examples of syntribos configs; currently only Keystone)
    - ``templates/`` (examples of request templates; currently only Keystone/Solum)
- ``scripts/`` (?)
- ``syntribos/`` (core syntribos code)
    - ``clients/`` (clients for making calls, e.g. HTTP)
        - ``http/`` (clients for making HTTP requests)
    - ``extensions/`` (extensions that can be called in request templates)
        - ``identity/`` (extension for interacting with Keystone/identity)
        - ``random_data/`` (extension for generating random test data)
    - ``formatters/`` (output formatters, e.g. JSON, XML/XUnit)
    - ``tests/`` (location of tests that syntribos can run against a target)
        - ``auth/`` (tests related to authentication/authorization)
        - ``fuzz/`` (tests that "fuzz" API requests)
    - ``utils/`` (utility methods)
- ``tests/unit/`` (unittests for testing syntribos itself)
