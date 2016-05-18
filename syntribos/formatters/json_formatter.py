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
        machine_output = dict({'failures': {}, 'errors': [], 'stats': []})

        # reports errors
        for test, error in self.results.errors:
            machine_output['errors'].append(
                {
                    'test': self.results.getDescription(test),
                    'error': error
                })

        # reports failures
        # Gets list of [issues] by flattening list of [(test, [issues])]
        issues = [issue for test, failures in self.results.failures
                  for issue in failures]
        for issue in issues:
            target = issue.target
            path = issue.path
            url = "{0}{1}".format(target, path)
            test_type = issue.test_type

            if issue.impacted_parameter:
                # Only fuzz tests have an ImpactedParameter
                method = issue.impacted_parameter.method
                loc = issue.impacted_parameter.location
                name = issue.impacted_parameter.name
                content_type = issue.content_type
                if loc == "data":
                    param = "{0} - {1}:{2}|{3}".format(method, loc,
                                                       content_type, name)
                else:
                    param = "{0} - {1}|{2}".format(method, loc, name)
            defect_type = issue.defect_type

            if url not in machine_output['failures']:
                machine_output['failures'][url] = {}

            issues_by_url = machine_output['failures'][url]
            if test_type not in issues_by_url:
                issues_by_url[test_type] = {}

            issues_by_test = issues_by_url[test_type]
            if issue.impacted_parameter:
                if param not in issues_by_test:
                    issues_by_test[param] = {}

                issues_by_param = issues_by_test[param]
                if defect_type not in issues_by_param:
                    issues_by_param[defect_type] = issue.get_details()
                    issues_by_param[defect_type]['payloads'] = set(
                        [issue.impacted_parameter.trunc_fuzz_string])

                issues_by_defect = issues_by_param[defect_type]
                issues_by_defect['payloads'].add(
                    issue.impacted_parameter.trunc_fuzz_string)
            else:
                if defect_type not in issues_by_test:
                    issues_by_test[defect_type] = issue.get_details()

        # reports stats
        machine_output['stats'] = self.results.stats

        output = json.dumps(machine_output, sort_keys=True,
                            indent=2, separators=(',', ': '), cls=SetEncoder)

        self.results.stream.write(output)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
