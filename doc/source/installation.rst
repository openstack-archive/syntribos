============
Installation
============

Syntribos can be installed directly from `pypi with pip <https://pypi.python.org/pypi/pip>`__

::

   pip install syntribos

If you want the latest changes, you could install syntribos from `source <https://www.github.com/openstack/syntribos.git>`__
with `pip <https://pypi.python.org/pypi/pip>`__.

-  Clone the repository

::

   $ git clone https://github.com/openstack/syntribos.git

- cd to the directory and install with pip

::

   $ cd syntribos
   $ pip install .

======================================
Initializing the syntribos Environment
======================================

Once syntribos is installed, you must initialize the syntribos environment.
This can be done manually, or via the ``init`` command. 

::

    $ syntribos init


If you'd like to specify a custom root for syntribos to be installed in,
specify the ``--custom_install_root`` flag after ``init``. This will skip
syntribos' prompts for information from the terminal, which can be handy for
Jenkins jobs and other situations where user input cannot be retrieved.

If you've already run the ``init`` command but want to start over with a fresh
environment, you can specify the ``--force`` flag to overwrite existing files.
The ``--custom_install_root`` and ``--force`` flags can be combined to overwrite
files in a custom install root.

**Example:**

::

    $ syntribos init --custom_install_root /your/custom/path --force


