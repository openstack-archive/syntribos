"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys
import argparse

from cafe.drivers.unittest.arguments import ConfigAction


class InputType(object):
    def __init__(self, mode, bufsize):
        self._mode = mode
        self._bufsize = bufsize

    def __call__(self, string):
        if string == '-':
            fp = sys.stdin
            yield fp.name, fp.read()
        elif os.path.isdir(string):
            for path, _, files in os.walk(string):
                for file_ in files:
                    file_path = os.path.join(path, file_)
                    fp = open(file_path, self._mode, self._bufsize)
                    yield file_, fp.read()
                    fp.close()
        elif os.path.isfile(string):
            try:
                fp = open(string, self._mode, self._bufsize)
                yield os.path.split(fp.name)[1], fp.read()
                fp.close()
            except Exception as e:
                message = "can't open {}:{}"
                raise Exception(message.format(string, e))
        else:
            message = "can't open {} not a readable file or dir"
            raise Exception(message.format(string))


class SyntribosCLI(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(SyntribosCLI, self).__init__(*args, **kwargs)
        self._add_args()

    def _add_args(self):
        self.add_argument(
            "config", metavar="<config>", action=ConfigAction,
            help="test config.  Looks in the ~/.opencafe/configs directory"
            "Example: compute/dev.environ")

        self.add_argument(
            "input", metavar="<input_file>", type=InputType('r', 0),
            help="<input file|directory of files|-(for stdin)>")

        self.add_argument(
            "-t", "--test-types", metavar="TEST_TYPES", nargs="*",
            default=[""], help="Test types to run against api")

        self.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="unittest verbose pass through")

        self.add_argument(
            "--dry-run",
            action="store_true",
            help="Dry Run gets all test cases but does not run them")
