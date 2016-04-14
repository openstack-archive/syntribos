# Copyright 2016 Rackspace
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
import json


class JSONFormatter(object):

    def __init__(self, results):
        self.results = results

    def report(self):
        machine_output = dict({'results': [], 'errors': [], 'stats': []})

        # reports errors
        for test, error in self.results.errors:
            machine_output['errors'].append(
                {
                    'test': self.results.getDescription(test),
                    'error': error
                })

        # reports failures
        for test, failure in self.results.failures:
            machine_output['results'].append(
                {
                    'test': self.results.getDescription(test),
                    'failure': failure
                })

        output = json.dumps(machine_output, sort_keys=True,
                            indent=2, separators=(',', ': '))

        # TODO(mdong): Stats

        self.results.stream.write(output)
