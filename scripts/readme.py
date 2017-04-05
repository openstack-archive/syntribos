#!/usr/bin/env python
# Copyright 2016 Intel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

repository_tags = """
========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/syntribos.svg
    :target: http://governance.openstack.org/reference/tags/index.html


.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
    :target: http://docs.openstack.org/developer/syntribos/

.. image:: http://img.shields.io/pypi/v/syntribos.svg
    :target: http://pypi.python.org/pypi/syntribos/

.. image:: http://img.shields.io/pypi/pyversions/syntribos.svg
        :target: http://pypi.python.org/pypi/syntribos/

.. image:: http://img.shields.io/pypi/wheel/syntribos.svg
        :target: http://pypi.python.org/pypi/syntribos/

.. image:: http://img.shields.io/irc/%23openstack-security.png
        :target: http://webchat.freenode.net/?channels=openstack-security


"""


def find_docs():
    """Yields files as per the whitelist."""
    loc = "../doc/source/{}.rst"
    whitelist = [
        "about", "installation",
        "configuration", "commands",
        "running", "logging",
        "test-anatomy", "unittests",
        "contributing"]

    for fname in whitelist:
        fpath = loc.format(fname)
        if os.path.isfile(fpath):
            yield fpath


def concat_docs():
    """Concatinates files yielded by the generator `find_docs`."""
    file_path = os.path.dirname(os.path.realpath(__file__))
    head, tail = os.path.split(file_path)
    outfile = head + "/README.rst"
    if not os.path.isfile(outfile):
        print("../README.rst not found, exiting!")
        exit(1)
    with open(outfile, 'w') as readme_handle:
        readme_handle.write(repository_tags)
        for doc in find_docs():
            with open(doc, 'r') as doc_handle:
                for line in doc_handle:
                    readme_handle.write(line)
                readme_handle.write("\n")


if __name__ == '__main__':
    """Generate README.rst from docs."""
    concat_docs()
    print("\nREADME.rst created!\n")
