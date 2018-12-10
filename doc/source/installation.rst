============
Installation
============

Syntribos can be installed directly from `pypi with pip <https://pypi.python.org/pypi/pip>`__.

::

   pip install syntribos

For the latest changes, install syntribos from `source <https://www.github.com/openstack/syntribos.git>`__
with `pip <https://pypi.python.org/pypi/pip>`__.

Clone the repository::

   $ git clone https://github.com/openstack/syntribos.git

Change directory into the repository clone and install with pip::

   $ cd syntribos
   $ pip install .

======================================
Initializing the syntribos Environment
======================================

Once syntribos is installed, you must initialize the syntribos environment.
This can be done manually, or with the ``init`` command.

::

    $ syntribos init

.. Note::
    By default, ``syntribos init`` fetches a set of default payload files
    from a `remote repository <https://github.com/openstack/syntribos-payloads>`_
    maintained by our development team. These payload files are necessary for
    our fuzz tests to run. To disable this behavior, run syntribos with the
    ``--no_downloads`` flag. Payload files can also be fetched by running
    ``syntribos download --payloads`` at any time.

To specify a custom root for syntribos to be installed in,
specify the ``--custom_root`` flag. This will skip
prompts for information from the terminal, which can be handy for
Jenkins jobs and other situations where user input cannot be retrieved.

If you've already run the ``init`` command but want to start over with a fresh
environment, you can specify the ``--force`` flag to overwrite existing files.
The ``--custom_root`` and ``--force`` flags can be combined to
overwrite files in a custom install root.

Note: if you install syntribos to a custom install root, you must supply the
``--custom_root`` flag when running syntribos.

**Example:**

::

    $ syntribos --custom_root /your/custom/path init --force
    $ syntribos --custom_root /your/custom/path run


