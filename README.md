CloudCAFE, An Open CAFE Implementation for OpenStack
====================================================

<pre>
   _ _ _
  ( `   )_
 (    )   `)  _
(____(__.___`)__)

    ( (
       ) )
    .........
    |       |___
    |       |_  |
    |  :-)  |_| |
    |       |___|
    |_______|
=== CloudCAFE ===
= An Open CAFE Implementation =
</pre>

CloudCAFE is an implementation of the [Open CAFE Framework](https://github.com/stackforge/opencafe) specifically
designed to test deployed versions of [OpenStack](http://http://www.openstack.org/). It is built using the
[Open CAFE Core](https://github.com/stackforge/opencafe).


Supported Operating Systems
---------------------------
CloudCAFE has been developed primarily in Linux and Mac environments, however it supports installation and
execution on Windows.


Installation
------------
CloudCAFE can be [installed with pip](https://pypi.python.org/pypi/pip) from the git repository after it is cloned to
a local machine.

* First follow the README instructions to install [Open CAFE Core](https://github.com/stackforge/opencafe).
* Clone this repository to your local machine.
* CD to the cloned cloudcafe repository directory.
* Run `pip install . --upgrade` so that pip will auto-install all other dependencies.


Configuration
--------------
CloudCAFE works in tandem with the [Open CAFE Core](https://github.com/stackforge/opencafe) cafe-runner. This
installation of CloudCAFE includes a reference configuration for each of the CloudCAFE supported OpenStack products.
Configurations will be installed to `<USER_HOME>/.cloudcafe/configs/<PRODUCT>`.

To use CloudCAFE you **will need to create/install your own configurations** based on the reference configs pointing
to your deployment of OpenStack.

At this stage you will have the Open CAFE Core engine and the CloudCAFE Framework implementation. From this point you
are ready to:

1. Write entirely new tests using the CloudCAFE Framework,

   *or...*

2. Install the [CloudRoast Test Repository](https://github.com/stackforge/cloudroast), an open source body of
   OpenStack automated tests written with CloudCAFE that can be executed or extended.


Logging
-------
CloudCAFE leverages the logging capabilities of the CAFE Core engine. If tests are executed with the built-in
cafe-runner, runtime logs will be output to `<USER_HOME>/.cloudcafe/logs/<PRODUCT>/<CONFIGURATION>/<TIME_STAMP>`.
In addition, tests built from the built-in CAFE unittest driver will generate csv statistics files in
`<USER_HOME>/.cloudcafe/logs/<PRODUCT>/<CONFIGURATION>/statistics` for each and ever execution of each and every test
case that provides metrics of execution over time for elapsed time, pass/fail rates, etc.


Basic CloudCAFE Package Anatomy
-------------------------------
Below is a short description of the top level CloudCAFE Packages.

* **cloudcafe**
  This is the root package for all things CloudCAFE.

* **common**
  Contains modules that extend the CAFE Core engine specific to OpenStack. This is the primary namespace for tools,
  data generators, common reporting classes, etc.

* **identity**
  OpenStack Identity Service plug-in based on CAFE Core extensions.

* **compute**
  OpenStack Compute plug-in based on CAFE Core extensions.

* **blockstorage**
  OpenStack Block Storage plug-in based on CAFE Core extensions.

* **objectstorage**
  OpenStack Object Storage plug-in based on CAFE Core extensions.


Join us
-------

* IRC: #cafehub on irc.freenode.net
* Mailing list: openstack-dev@lists.openstack.org
