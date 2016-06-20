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

import syntribos


class JSONFormatter(object):

    def __init__(self, results):
        self.results = results

    def report(self, min_severity, min_confidence):
        min_sev = syntribos.RANKING_VALUES[min_severity]
        min_conf = syntribos.RANKING_VALUES[min_confidence]
        machine_output = dict({'failures': {}, 'errors': [], 'stats': {}})
        machine_output['stats']['severity'] = {
            'UNDEFINED': 0, 'LOW': 0, 'MEDIUM': 0, 'HIGH': 0
        }

        severity_counter_dict = {}

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
            defect_type = issue.defect_type
            sev_rating = syntribos.RANKING[issue.severity]
            conf_rating = syntribos.RANKING[issue.confidence]

            defect_obj = {
                'description': issue.text,
                'severity': sev_rating
            }

            if defect_type not in severity_counter_dict:
                severity_counter_dict[defect_type] = defect_obj
                machine_output['stats']['severity'][sev_rating] += 1

            if url not in machine_output['failures']:
                if issue.severity >= min_sev and issue.confidence >= min_conf:
                    machine_output['failures'][url] = {}
                else:
                    continue

            issues_by_url = machine_output['failures'][url]
            if defect_type not in issues_by_url:
                if issue.severity >= min_sev and issue.confidence >= min_conf:
                    issues_by_url[defect_type] = defect_obj
                else:
                    continue

            issues_by_defect = issues_by_url[defect_type]
            if issue.impacted_parameter:
                # Only fuzz tests have an ImpactedParameter
                method = issue.impacted_parameter.method
                loc = issue.impacted_parameter.location
                name = issue.impacted_parameter.name
                content_type = issue.content_type
                payload_string = issue.impacted_parameter.trunc_fuzz_string

                param = {
                    'method': method,
                    'location': loc,
                    'variables': [name],
                }
                if loc == "data":
                    param['type'] = content_type

                payload_obj = {
                    'strings': [payload_string],
                    'param': param,
                    'confidence': conf_rating
                }
                if 'payloads' not in issues_by_defect:
                    issues_by_defect['payloads'] = [payload_obj]
                else:
                    is_not_duplicate_payload = True

                    for p in issues_by_defect['payloads']:

                        if (p['param']['method'] == method and
                                p['param']['location'] == loc):

                            if payload_string not in p['strings']:
                                p['strings'].append(payload_string)

                            if name not in p['param']['variables']:
                                p['param']['variables'].append(name)

                            is_not_duplicate_payload = False
                            break
                    if is_not_duplicate_payload:
                        issues_by_defect['payloads'].append(payload_obj)

            else:
                issues_by_defect['confidence'] = conf_rating

        output = json.dumps(machine_output, sort_keys=True,
                            indent=2, separators=(',', ': '))

        self.results.stream.write(output)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
