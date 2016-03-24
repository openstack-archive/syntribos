Installation
============

Syntribos can be `installed with
pip <https://pypi.python.org/pypi/pip>`__ from the git repository.

-  Clone the repository and install it using pip

::

   $ git clone https://github.com/openstack/syntribos.git
   $ cd syntribos
   $ pip install . --upgrade

-  To enable autocomplete for Syntribos, run the command.

::

   $ . scripts/syntribos-completion

-  Create a directory named .opencafe in the user's home directory, or in the case of a python virtualenv, in the virtualenv root folder.

::

   $ cafe-config init

-  Install the http library that gives you the minimum plugins required to use Syntribos.

::

   $ cafe-config plugins install http 
