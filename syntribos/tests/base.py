import os

from cafe.engine.models.data_interfaces import ConfigSectionInterface
from cafe.engine.http.client import HTTPClient


data_dir = os.environ.get("CAFE_DATA_DIR_PATH")
test_table = {}


class TestType(type):
    def __new__(cls, cls_name, cls_parents, cls_attr):
        new_class = super(TestType, cls).__new__(
            cls, cls_name, cls_parents, cls_attr)
        test_name = getattr(new_class, "test_name", None)
        if test_name is not None:
            if test_name in test_table:
                msg = "Test name already used {}".format(test_name)
                raise Exception(msg)
            test_table[test_name] = new_class
        return new_class


class BaseTestConfig(ConfigSectionInterface):
    SECTION_NAME = None

    @property
    def percent(self):
        return self.get("percent")


class BaseTest(object):
    """
    Base for building new tests
    """
    __metaclass__ = TestType
    test_name = None
    test_type = None
    filename = None
    config = None

    @classmethod
    def validate_test(cls, response):
        return all([
            response.status_code < 500,
            cls.validate_length(response, cls.config.percent)])

    @classmethod
    def get_strings(cls):
        path = os.path.join(data_dir, cls.filename)
        return open(path, "rb")

    @classmethod
    def validate_length(cls, response, percent=5):
        if getattr(cls, "init_response", False) is False:
            raise NotImplemented
        resp_len = len(response.content)
        req_len = len(response.request.data)
        iresp_len = len(cls.init_response.content)
        ireq_len = len(cls.init_response.request.data)
        request_diff = req_len - ireq_len
        response_diff = resp_len - iresp_len
        if request_diff == response_diff:
            return True
        elif resp_len == iresp_len:
            return True
        elif percent:
            if abs(float(response_diff) / iresp_len) <= (percent / 100.0):
                return True
        return False

    @classmethod
    def run_test(cls, request, init_response):
        client = HTTPClient()
        r = client.request(
            method=request.method, url=request.url, headers=request.headers,
            params=request.params, data=request.data)
        return cls.validate_test(r, init_response)
