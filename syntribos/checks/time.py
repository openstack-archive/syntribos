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
from oslo_config import cfg

import syntribos.signal

CONF = cfg.CONF


def percentage_difference(test):
    """Validates time taken for two responses

    Compares the elapsed time of a fuzzed response with a response to the
    baseline request. If the response takes longer than expected, returns
    a `TimePercentageDiffSignal`

    :returns: SynSignal or None
    """
    check_name = "TIME_DIFF"
    data = {
        "req1": test.init_req,
        "req2": test.test_req,
        "resp1": test.init_resp,
        "resp2": test.test_resp,
        "resp1_time": test.init_resp.elapsed.total_seconds(),
        "resp2_time": test.test_resp.elapsed.total_seconds()
    }
    data["time_diff"] = data["resp2_time"] - data["resp1_time"]
    # CCNEILL: This is hacky. Exact match != 100% (due to +1)
    data["percent_diff"] = abs(
        float(data["time_diff"]) / (data["resp1_time"] + 1)) * 100
    data["dir"] = "UNDER"
    if data["resp1_time"] < data["resp2_time"]:
        data["dir"] = "OVER"

    if data["percent_diff"] < CONF.test.time_diff_percent:
        # Difference not larger than configured percentage
        return None

    text = ("Validate Time Differential:\n"
            "\tResponse 1 elapsed time: {0}\n"
            "\tResponse 2 elapsed time: {1}\n"
            "\tResponse difference: {2}\n"
            "\tPercent difference: {3}%\n"
            "\tDifference direction: {4}"
            "\tConfig percent: {5}\n").format(
                data["resp1_time"], data["resp2_time"], data["time_diff"],
                data["percent_diff"], data["dir"], CONF.test.time_diff_percent)

    slug = "TIME_DIFF_{dir}".format(dir=data["dir"])

    return syntribos.signal.SynSignal(
        text=text, slug=slug, strength=1.0, data=data, check_name=check_name)


def absolute_time(test):
    """Checks response takes less than `config.max_time` seconds

    :returns: SynSignal or None
    """
    check_name = "ABSOLUTE_TIME"

    if not test.init_signals.ran_check(check_name):
        resp = test.init_resp
    else:
        resp = test.test_resp

    data = {
        "request": resp.request,
        "response": resp,
        "elapsed": resp.elapsed.total_seconds(),
        "max_time": CONF.test.max_time
    }

    if data["elapsed"] < data["max_time"]:
        return None

    text = ("Check that response time doesn't exceed test.max_time:\n"
            "\tMax time: {0}\n"
            "\tElapsed time: {1}\n").format(data["elapsed"], data["max_time"])

    slug = "TIME_OVER_MAX"
    tags = ["CONNECTION_TIMEOUT"]

    return syntribos.signal.SynSignal(
        text=text,
        slug=slug,
        strength=1.0,
        tags=tags,
        data=data,
        check_name=check_name)
