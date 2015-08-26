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

from syntribos.clients.http import client
from syntribos.tests import base
from syntribos.tests.fuzz.config import BaseFuzzConfig
from syntribos.tests.fuzz.datagen import FuzzParser


data_dir = os.environ.get("CAFE_DATA_DIR_PATH")


class BaseFuzzTestCase(base.BaseTestCase):
    config = BaseFuzzConfig()
    client = client()
    failure_keys = None
    success_keys = None

    @classmethod
    def validate_length(cls):
        if getattr(cls, "init_response", False) is False:
            raise NotImplemented
        init_req_len = len(cls.init_response.request.body or "")
        init_resp_len = len(cls.init_response.content or "")
        req_len = len(cls.resp.request.body or "")
        resp_len = len(cls.resp.content or "")
        request_diff = req_len - init_req_len
        response_diff = resp_len - init_resp_len
        percent_diff = abs(float(response_diff) / (init_resp_len + 1)) * 100
        msg = (
            "Validate Length:\n"
            "\tInitial request length: {0}\n"
            "\tInitial response length: {1}\n"
            "\tRequest length: {2}\n"
            "\tResponse length: {3}\n"
            "\tRequest difference: {4}\n"
            "\tResponse difference: {5}\n"
            "\tPercent difference: {6}\n"
            "\tConfig percent: {7}\n").format(
            init_req_len, init_resp_len, req_len, resp_len, request_diff,
            response_diff, percent_diff, cls.config.percent)
        cls.fixture_log.debug(msg)
        if request_diff == response_diff:
            return True
        elif resp_len == init_resp_len:
            return True
        elif cls.config.percent:
            if percent_diff <= cls.config.percent:
                return True
        return False

    @classmethod
    def _get_strings(cls, file_name=None):
        path = os.path.join(data_dir, file_name or cls.data_key)
        with open(path, "rb") as fp:
            return fp.read().splitlines()

    @classmethod
    def data_driven_failure_cases(cls):
        if cls.failure_keys is None:
            return
        for line in cls.failure_keys:
            cls.assertNotIn(line, cls.resp.content)

    @classmethod
    def data_driven_pass_cases(cls):
        if cls.success_keys is None:
            return True
        assert any(True for s in cls.success_keys if s in cls.resp.content)

    @classmethod
    def setUpClass(cls):
        """being used as a setup test not"""
        super(BaseFuzzTestCase, cls).setUpClass()
        cls.resp = cls.client.request(
            method=cls.request.method, url=cls.request.url,
            headers=cls.request.headers, params=cls.request.params,
            data=cls.request.data)

    def test_case(self):
        self.assertTrue(self.resp.status_code < 500)
        self.assertTrue(self.validate_length())
        self.data_driven_failure_cases()
        self.data_driven_pass_cases()

    @classmethod
    def get_test_cases(cls, filename, file_content):
        # maybe move this block to base.py
        request_obj = FuzzParser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT"))
        prepared_copy = request_obj.get_prepared_copy()
        cls.init_response = cls.client.send_request(prepared_copy)
        # end block

        prefix_name = "{filename}_{test_name}_{fuzz_file}_".format(
            filename=filename, test_name=cls.test_name, fuzz_file=cls.data_key)
        for fuzz_name, request in request_obj.fuzz_request(
                cls._get_strings(), cls.test_type, prefix_name):
            yield cls.extend_class(fuzz_name, {"request": request})
