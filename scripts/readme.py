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


def find_docs():
    """Yields files as per the whitelist."""
    loc = "../doc/source/{}.rst"
    whitelist = [
        "about", "installation",
        "configuration", "commands",
        "running", "logging",
        "test.anatomy", "unittests",
        "contributing"]

    for fname in whitelist:
        fpath = loc.format(fname)
        if os.path.isfile(fpath):
            yield fpath


def concat_docs():
    """Concatinates files yielded by the generator `find_docs`."""
    outfile = "../README.rst"
    if not os.path.isfile(outfile):
        print("../README.rst not found, exiting!")
        exit(1)
    with open(outfile, 'w') as readme_handle:
        for doc in find_docs():
            with open(doc, 'r') as doc_handle:
                for line in doc_handle:
                    readme_handle.write(line)
                readme_handle.write("\n")


if __name__ == '__main__':
    """Generate README.rst from docs."""
    concat_docs()
    print("\nREADME.rst created!\n")
