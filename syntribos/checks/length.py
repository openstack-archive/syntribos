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
    """Validates length of two responses

    Compares the length of a fuzzed response with a response to the
    baseline request. If the response is longer than expected, returns
    a `LengthPercentageDiffSignal`

    :returns: SynSignal or None
    """
    check_name = "LENGTH_DIFF"
    data = {
        "req1": test.init_req,
        "req2": test.test_req,
        "resp1": test.init_resp,
        "resp2": test.test_resp,
        "req1_len": len(test.init_req.body or ""),
        "req2_len": len(test.test_req.body or ""),
        "resp1_len": len(test.init_resp.content or ""),
        "resp2_len": len(test.test_resp.content or ""),
    }
    data["req_diff"] = data["req2_len"] - data["req1_len"]
    data["resp_diff"] = data["resp2_len"] - data["resp1_len"]
    data["percent_diff"] = abs(
        float(data["resp_diff"]) / (data["resp1_len"] + 1)) * 100
    data["dir"] = "UNDER" if data["resp1_len"] > data["resp2_len"] else "OVER"

    if data["resp1_len"] == data["resp2_len"]:
        # No difference in response lengths
        return None
    elif data["req_diff"] == data["resp_diff"]:
        # Response difference accounted for by difference in request lengths
        return None
    elif data["percent_diff"] < CONF.test.length_diff_percent:
        # Difference not larger than configured percentage
        return None

    text = (
        "Validate Length:\n"
        "\tRequest 1 length: {0}\n"
        "\tResponse 1 length: {1}\n"
        "\tRequest 2 length: {2}\n"
        "\tResponse 2 length: {3}\n"
        "\tRequest difference: {4}\n"
        "\tResponse difference: {5}\n"
        "\tPercent difference: {6}%\n"
        "\tDifference direction: {7}"
        "\tConfig percent: {8}\n").format(
            data["req1_len"], data["resp1_len"], data["req2_len"],
            data["resp2_len"], data["req_diff"], data["resp_diff"],
            data["percent_diff"], data["dir"], CONF.test.length_diff_percent)

    slug = "LENGTH_DIFF_{dir}".format(dir=data["dir"])

    return syntribos.signal.SynSignal(
        text=text, slug=slug, strength=1.0, data=data, check_name=check_name)


def max_body_length(test):
    """Checks if the response body length is more than max size in the config.

    Checks the response body to see if the length is more than the given length
     in the config. If it is, returns a Signal.

    :returns: SynSignal or None
    """
    check_name = "MAX_LENGTH"
    if test.init_signals.ran_check(check_name):
        resp = test.init_resp
    else:
        resp = test.test_resp
    data = {
        "req": resp.request,
        "resp": resp,
        "req_len": len(resp.request.body or ""),
        "resp_len": len(resp.content or ""),
    }
    text = ("Length:\n"
            "\tRequest length: {0}\n"
            "\tResponse length: {1}\n".format(data["req_len"],
                                              data["resp_len"]))
    slug = "OVER_MAX_LENGTH"

    if data["resp_len"] > CONF.test.max_length:
        return syntribos.signal.SynSignal(
            text=text,
            slug=slug,
            strength=1.0,
            data=data,
            check_name=check_name)
