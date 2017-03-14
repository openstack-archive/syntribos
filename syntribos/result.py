# Copyright 2015 Rackspace
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
import time
import unittest

from oslo_config import cfg

import syntribos
from syntribos._i18n import _
from syntribos.formatters.json_formatter import JSONFormatter
from syntribos.runner import Runner
import syntribos.utils.remotes

CONF = cfg.CONF


class IssueTestResult(unittest.TextTestResult):
    """Custom unnittest results holder class

    This class aggregates :class:`syntribos.issue.Issue` objects from all the
    tests as they run
    """
    output = {"failures": {}, "errors": [], "stats": {}}
    output["stats"]["severity"] = {
        "UNDEFINED": 0,
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0
    }
    stats = {"errors": 0, "failures": 0, "successes": 0}
    severity_counter_dict = {}
    testsRunSinceLastPrint = 0
    failure_id = 0

    def addFailure(self, test, err):
        """Adds issues to data structures

        Appends issues to the result's list of failures, as well as updates the
        stats for the result. Each failure in the list of failures takes the
        form:

        .. code-block:: json

            {
              "url": "host.com/blah",
              "type": "500_error",
              "description": "500 errors r bad, mkay?",
              "failure_id": 1234,
              "instances": [
                {
                  "confidence": "HIGH",
                  "param": {
                    "location": "headers",
                    "method": "POST",
                    "variables": [
                      "Content-Type"
                    ]
                  },
                  "strings": [
                    "derp"
                  ],
                  "severity": "LOW",
                  "signals": {
                    "diff_signals": [],
                    "init_signals": [],
                    "test_signals": []
                  }
                }
              ]
            }

        :param test: The test that has failed
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        :param tuple err: Tuple of format ``(type, value, traceback)``
        """
        for issue in test.failures:
            defect_type = issue.defect_type
            if any([
                    True for x in CONF.syntribos.exclude_results
                    if x and x in defect_type
            ]):
                continue

            min_sev = syntribos.RANKING_VALUES[CONF.min_severity]
            min_conf = syntribos.RANKING_VALUES[CONF.min_confidence]
            if issue.severity < min_sev or issue.confidence < min_conf:
                continue

            target = issue.target
            path = issue.path
            url = "{0}{1}".format(target, path)
            description = issue.description
            failure_obj = None

            for f in self.failures:
                if (f["url"] == url and f["defect_type"] == defect_type and
                        f["description"] == description):
                    failure_obj = f
                    break
            if not failure_obj:
                failure_obj = {
                    "url": url,
                    "defect_type": defect_type,
                    "description": description,
                    "failure_id": self.failure_id,
                    "instances": []
                }
                self.failures.append(failure_obj)
                self.failure_id += 1

            signals = {}
            if issue.init_signals:
                signals["init_signals"] = set(
                    [s.slug for s in issue.init_signals])
            if issue.test_signals:
                signals["test_signals"] = set(
                    [s.slug for s in issue.test_signals])
            if issue.diff_signals:
                signals["diff_signals"] = set(
                    [s.slug for s in issue.diff_signals])
            sev_rating = syntribos.RANKING[issue.severity]
            conf_rating = syntribos.RANKING[issue.confidence]

            if issue.impacted_parameter:
                method = issue.impacted_parameter.method
                loc = issue.impacted_parameter.location
                name = issue.impacted_parameter.name
                content_type = issue.content_type
                payload_string = issue.impacted_parameter.trunc_fuzz_string

                param = {
                    "method": method,
                    "location": loc,
                }
                if loc == "data":
                    param["type"] = content_type

                instance_obj = None
                for i in failure_obj["instances"]:
                    if (i["confidence"] == conf_rating and
                            i["severity"] == sev_rating and
                            i["param"]["method"] == method and
                            i["param"]["location"] == loc):

                        i["param"]["variables"].add(name)
                        for sig_type in signals:
                            if sig_type in i["signals"]:
                                i["signals"][sig_type].update(signals[
                                    sig_type])
                            else:
                                i["signals"][sig_type] = signals[sig_type]
                        i["strings"].add(payload_string)
                        instance_obj = i
                        break

                if not instance_obj:
                    param["variables"] = set([name])
                    instance_obj = {
                        "confidence": conf_rating,
                        "severity": sev_rating,
                        "param": param,
                        "strings": set([payload_string]),
                        "signals": signals
                    }
                    failure_obj["instances"].append(instance_obj)
                    self.stats["failures"] += 1
                    self.output["stats"]["severity"][sev_rating] += 1
            else:
                instance_obj = None
                for i in failure_obj["instances"]:
                    if (i["confidence"] == conf_rating and
                            i["severity"] == sev_rating):
                        for sig_type in signals:
                            if sig_type in i["signals"]:
                                i["signals"][sig_type].update(signals[
                                    sig_type])
                            else:
                                i["signals"][sig_type] = signals[sig_type]
                        instance_obj = i
                        break
                if not instance_obj:
                    instance_obj = {
                        "confidence": conf_rating,
                        "severity": sev_rating,
                        "signals": signals
                    }
                    failure_obj["instances"].append(instance_obj)
                    self.stats["failures"] += 1
                    self.output["stats"]["severity"][sev_rating] += 1

    def addError(self, test, err):
        """Duplicates parent class addError functionality.

        :param test: The test that encountered an error
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        :param err:
        :type tuple: Tuple of format ``(type, value, traceback)``
        """
        self.errors.append({
            "test": self.getDescription(test),
            "error": self._exc_info_to_string(err, test)
        })
        self.stats["errors"] += 1

    def addSuccess(self, test):
        """Duplicates parent class addSuccess functionality.

        :param test: The test that was run
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        """
        self.stats["successes"] += 1

    def printErrors(self, output_format):
        """Print out each :class:`syntribos.issue.Issue` that was encountered

        :param str output_format: Either "json" or "xml"
        """
        self.output["errors"] = self.errors
        self.output["failures"] = self.failures
        formatter_types = {"json": JSONFormatter(self)}
        formatter = formatter_types[output_format]
        formatter.report(self.output)

    def print_result(self, start_time):
        """Prints test summary/stats (e.g. # failures) to stdout."""
        self.printErrors(CONF.output_format)
        self.print_log_path_and_stats(start_time)

    def print_log_path_and_stats(self, start_time):
        """Print the path to the log folder for this run."""
        test_log = Runner.log_path
        run_time = time.time() - start_time
        num_fail = self.stats["failures"]
        num_err = self.stats["errors"]
        print("\n{sep}\nTotal: Ran {num} test{suff} in {time:.3f}s".format(
            sep=syntribos.SEP,
            num=self.testsRun,
            suff="s" * bool(self.testsRun - 1),
            time=run_time))
        print("Total: {f} failure{fsuff} and {e} error{esuff}".format(
            f=num_fail,
            e=num_err,
            fsuff="s" * bool(num_fail - 1),
            esuff="s" * bool(num_err - 1)))
        if test_log:
            print(syntribos.SEP)
            print(_("LOG PATH...: %s") % test_log)
            print(syntribos.SEP)
