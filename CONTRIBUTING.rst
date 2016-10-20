Syntribos Contributing Guidelines
=================================

1. Follow all the `OpenStack Style Guidelines <http://docs.openstack.org/developer/hacking/>`__
   (e.g. PEP8, Py3 compatibility)
2. All new classes/functions should have appropriate docstrings in
   `RST format <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`__
3. All new code should have appropriate unittests (place them in the
   ``tests/unit`` folder)
4. No new code will be accepted if it adds a new dependency on OpenCAFE, or adds
   on top of existing CAFE functionality IF it cannot stand on its own without
   CAFE.

Anyone wanting to contribute to OpenStack must follow
`the OpenStack development workflow <http://docs.openstack.org/infra/manual/developers.html#development-workflow>`__

All changes should be submitted through the code review process in Gerrit
described above. All pull requests on Github will be closed/ignored.

Bugs should be filed on the `syntribos launchpad site <https://bugs.launchpad.net/syntribos>`__,
and not on Github. All Github issues will be closed/ignored.

Breaking changes, feature requests, and other unprioritized work should first be
submitted as a blueprint `here <https://blueprints.launchpad.net/syntribos>`__
for review.
