============
Unit testing
============

To execute unit tests automatically, navigate to the ``syntribos`` root
directory and install the test requirements.

::

    $ pip install -r test-requirements.txt

Now, run the ``unittest`` as below:

::

    $ python -m unittest discover tests/unit -p "test_*.py"

If you have configured tox you could also run the following:

::

    $ tox -e py27
    $ tox -e py35

This will run all the unit tests and give you a result output
containing the status and coverage details of each test.
