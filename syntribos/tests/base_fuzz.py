import os

from cafe.engine.http.client import HTTPClient
from cafe.engine.models.data_interfaces import ConfigSectionInterface

from syntribos.request_creator import RequestCreator
from syntribos.tests import base

data_dir = os.environ.get("CAFE_DATA_DIR_PATH")


class BaseFuzzConfig(ConfigSectionInterface):
    SECTION_NAME = "FUZZ"

    @property
    def percent(self):
        return self.get("percent")


class BaseFuzzTestCase(base.BaseTest):
    config = base.BaseTestConfig()
    client = HTTPClient()

    @classmethod
    def validate_length(cls):
        if getattr(cls, "init_response", False) is False:
            raise NotImplemented
        resp_len = len(cls.resp.content)
        req_len = len(cls.resp.request.data)
        iresp_len = len(cls.init_response.content)
        ireq_len = len(cls.init_response.request.data)
        request_diff = req_len - ireq_len
        response_diff = resp_len - iresp_len
        if request_diff == response_diff:
            return True
        elif resp_len == iresp_len:
            return True
        elif cls.config.percent:
            if abs(float(response_diff) / iresp_len) <= (
                    cls.config.percent / 100.0):
                return True
        return False

    @classmethod
    def get_strings(cls):
        path = os.path.join(data_dir, cls.data_key)
        return open(path, "rb")

    @classmethod
    def setupUpClass(cls):
        cls.config = BaseFuzzConfig()
        cls.resp = cls.client.request(
            method=cls.request.method, url=cls.request.url,
            headers=cls.request.headers, params=cls.request.params,
            data=cls.request.data)

    def test_case(self):
        return all([
            self.resp.status_code < 500,
            self.validate_length()])

    @classmethod
    def get_test_cases(cls, request_string, config):
        request_obj = RequestCreator.create_request(
            request_string, config.endpoint)
        cls.init_response =
        if cls.test_type == "BODY":

        yield cls
