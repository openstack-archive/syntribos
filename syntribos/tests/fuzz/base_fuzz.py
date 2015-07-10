import os

from syntribos.clients.http import SynHTTPClient, RequestCreator
from syntribos.tests import base
from syntribos.tests.fuzz.config import BaseFuzzConfig
from syntribos.tests.fuzz.datagen import FuzzBehavior


data_dir = os.environ.get("CAFE_DATA_DIR_PATH")


class BaseFuzzTestCase(base.BaseTestCase):
    config = BaseFuzzConfig()
    client = SynHTTPClient()

    @classmethod
    def validate_length(cls):
        if getattr(cls, "init_response", False) is False:
            raise NotImplemented
        init_req_len = len(cls.init_response.request.body or "")
        init_resp_len = len(cls.init_response.content or "")
        req_len = len(cls.resp.content or "")
        resp_len = len(cls.resp.request.body or "")

        request_diff = req_len - init_req_len
        response_diff = resp_len - init_resp_len
        if request_diff == response_diff:
            return True
        elif resp_len == init_resp_len:
            return True
        elif cls.config.percent:
            if abs(float(response_diff) / init_resp_len) <= (
                    cls.config.percent / 100.0):
                return True
        return False

    @classmethod
    def _get_strings(cls):
        path = os.path.join(data_dir, cls.data_key)
        with open(path, "rb") as fp:
            return fp.read().splitlines()

    @classmethod
    def setUpClass(cls):
        """being used as a setup test not"""
        super(BaseFuzzTestCase, cls).setUpClass()
        print cls.request.url
        cls.resp = cls.client.request(
            method=cls.request.method, url=cls.request.url,
            headers=cls.request.headers, params=cls.request.params,
            data=cls.request.data)

    def test_case(self):
        self.assertTrue(self.resp.status_code < 500)
        self.assertTrue(self.validate_length())

    @classmethod
    def get_test_cases(cls, filename, file_content):
        # maybe move this block to base.py
        request_obj = RequestCreator.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT"))

        prepared_copy = request_obj.get_prepared_copy()
        print prepared_copy.data
        cls.init_response = cls.client.send_request(prepared_copy)
        # end block

        for fuzz_name, request in cls._get_fuzz_requests(
                request_obj, cls._get_strings()):
            full_name = "{filename}_{fuzz_name}".format(
                filename=filename, fuzz_name=fuzz_name)
            yield cls.extend_class(full_name, {"request": request})

    @classmethod
    def _get_fuzz_requests(cls, request, strings):
        prefix_name = "{test_name}_{fuzz_file}_".format(
            test_name=cls.test_name,
            fuzz_file=cls.data_key)
        for name, data in FuzzBehavior.fuzz_data(
                strings, getattr(request, cls.test_type),
                request.action_field, prefix_name):
            request_copy = request.get_copy()
            setattr(request_copy, cls.test_type, data)
            request_copy.prepare_request()
            yield name, request_copy
