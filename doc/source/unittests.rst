===================
Executing unittests
===================

To execute unittests automatically, navigate to the ``syntribos`` root
directory and install the test requirements.

::

    $ pip install -r test-requirements.txt

Now, run

::

    $ python -m unittest discover tests/unit -p "test_*.py"

If you have configured tox you could also do

::

    $ tox -e py27
    $ tox -e py35

This will run all the unittests and give you a result output
containing the status and coverage details of each test.
