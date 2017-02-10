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
import json
from xml.etree import ElementTree

import six
import testtools

from syntribos.clients.http.parser import RequestObject
from syntribos.clients.http import VariableObject
import syntribos.tests.fuzz.datagen as fuzz_datagen


action_field = "ACTION_FIELD:"
test_dict = {"a": {"b": "c", "ACTION_FIELD:d": "e"}}
test_dict_w_list = {"a": ["val", "val2", "val3"], "b": "c"}
test_json_str = '{"a": {"b": "c", "ACTION_FIELD:d": "e"}}'
test_params_obj = {"key": "val", "otherkey": "val2"}
endpoint = "http://test.com"
test_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
test_params = {"var1": "val1", "var2": "val2"}


def get_url(path):
    """Helper method to append endpoint and slash if necessary."""
    return "{endpoint}{sep}{path}".format(
        endpoint=endpoint,
        sep="/" if not path.startswith("/") else "",
        path=path)


def req(method, path, *args, **kwargs):
    """Helper method to create a RequestObject."""
    if not kwargs.get("headers"):
        kwargs["headers"] = test_headers
    if not kwargs.get("action_field"):
        kwargs["action_field"] = action_field
    return RequestObject(method, get_url(path), *args, **kwargs)


def get_req(path, *args, **kwargs):
    """Helper method to create a GET request."""
    return req("GET", path, *args, **kwargs)


def post_req(path, *args, **kwargs):
    """Helper method to create a POST request."""
    return req("POST", path, *args, **kwargs)


class FuzzDatagenUnittest(testtools.TestCase):

    def test_fuzz_data_dict(self):
        """Test _fuzz_data with a dict."""
        strings = ["test"]

        for i, d in enumerate(
                fuzz_datagen._fuzz_data(strings, test_dict, action_field,
                                        "unittest"), 1):
            name, model, stri, param_path = d
            self.assertEqual("unitteststr1_model{0}".format(i), name)
            self.assertEqual("e", model.get("a").get("ACTION_FIELD:d"))
            self.assertEqual("test", model.get("a").get("b"))
            self.assertEqual("test", stri)
            self.assertEqual("a/b", param_path)

    def test_fuzz_data_dict_with_list(self):
        """Test _fuzz_data with a dict containing a list."""
        strings = ["test"]
        expected = [
            {
                "a": ["test", "val2", "val3"],
                "b": "c"
            }, {
                "a": ["val", "test", "val3"],
                "b": "c"
            }, {
                "a": ["val", "val2", "test"],
                "b": "c"
            }, {
                "a": ["val", "val2", "val3"],
                "b": "test"
            }
        ]
        i = 0
        for i, result in enumerate(
                fuzz_datagen._fuzz_data(strings, test_dict_w_list,
                                        action_field, "unittest"), 1):
            name, model, string, param_path = result
            self.assertIn(model, expected)
            self.assertEqual("unitteststr1_model{0}".format(i), name)
        self.assertEqual(4, i)

    def test_fuzz_data_xml(self):
        """Test _fuzz_data_ with an XML element."""
        data = ElementTree.Element("a")
        sub_ele = ElementTree.Element("b")
        sub_ele.text = "c"
        sub_ele.attrib = {"name": "val"}
        sub_ele2 = ElementTree.Element("ACTION_FIELD:d")
        sub_ele2.text = "e"
        data.append(sub_ele)
        data.append(sub_ele2)
        strings = ["test"]

        contents = []
        expected_contents = [
            '<a><b name="val">test</b><ACTION_FIELD:d>e</ACTION_FIELD:d></a>',
            '<a><b name="test">c</b><ACTION_FIELD:d>e</ACTION_FIELD:d></a>'
        ]

        for i, d in enumerate(
                fuzz_datagen._fuzz_data(strings, data, "ACTION_FIELD:",
                                        "unittest"), 1):
            name, model, stri, param_path = d
            self.assertEqual("unitteststr1_model{0}".format(i), name)
            self.assertEqual("test", stri)
            if six.PY2:
                contents.append(ElementTree.tostring(model))
            else:
                contents.append(ElementTree.tostring(model).decode("utf-8"))
        self.assertEqual(expected_contents, contents)

    def test_fuzz_data_string(self):
        """Test _fuzz_data with a string like a URL."""
        data = "TEST_STRING/{ST}"
        strings = ["test"]

        for i, d in enumerate(
                fuzz_datagen._fuzz_data(strings, data, action_field,
                                        "unittest"), 1):
            name, model, stri, param_path = d
            self.assertEqual("unitteststr1_model{0}".format(i), name)
            self.assertEqual("TEST_STRING/test", model)
            self.assertEqual("test", stri)
            self.assertEqual("ST", param_path)

    def test_invalid_type(self):
        """Test _fuzz_data with a list (invalid type)."""
        data = set(["list", "of", "strings"])
        strings = ["test"]

        self.assertRaises(
            TypeError,
            fuzz_datagen._fuzz_data(strings, data, action_field, "unittest"))

    def test_str_combos_with_name(self):
        """Test building string combinations with 1 named URL variable."""
        data = "/api/v1/{key:val}"
        results = [
            d for d in fuzz_datagen._build_str_combinations("test", data)
        ]
        self.assertIn(("/api/v1/test", "key"), results)
        self.assertEqual(1, len(results))

    def test_fuzz_data_with_multiple_string_names(self):
        """Test _fuzz_data with 2 named URL variables."""
        strings = ["test", "test2"]
        data = "/api/v1/{key:val}/path/{otherkey:val2}"
        expected_results = [
            ("unitteststr1_model1", "/api/v1/test/path/{otherkey:val2}",
             "test", "key"),
            ("unitteststr1_model2", "/api/v1/{key:val}/path/test", "test",
             "otherkey"), ("unitteststr2_model1",
                           "/api/v1/test2/path/{otherkey:val2}", "test2",
                           "key"), ("unitteststr2_model2",
                                    "/api/v1/{key:val}/path/test2", "test2",
                                    "otherkey")
        ]
        results = [
            d
            for d in fuzz_datagen._fuzz_data(strings, data, action_field,
                                             "unittest")
        ]
        self.assertEqual(expected_results, results)

    def test_fuzz_data_with_one_named_one_unnamed(self):
        """Test _fuzz_data with 1 named, 1 unnamed URL variables."""
        strings = ["test", "test2"]
        data = "/api/v1/{key:val}/path/{otherkey}"
        expected_results = [
            ("unitteststr1_model1", "/api/v1/test/path/{otherkey}", "test",
             "key"), ("unitteststr1_model2", "/api/v1/{key:val}/path/test",
                      "test", "otherkey"),
            ("unitteststr2_model1", "/api/v1/test2/path/{otherkey}", "test2",
             "key"), ("unitteststr2_model2", "/api/v1/{key:val}/path/test2",
                      "test2", "otherkey")
        ]
        results = [
            d
            for d in fuzz_datagen._fuzz_data(strings, data, action_field,
                                             "unittest")
        ]
        self.assertEqual(expected_results, results)

    def test_post_fuzz_req_url_vars(self):
        """Test fuzz_request with 2 named URL params."""
        req = post_req("/api/v1/{key:val}/path/{otherkey:val2}")
        strings = ["test"]
        results = [
            d for d in fuzz_datagen.fuzz_request(req, strings, "url", "ut")
        ]
        req_objs = [r[1] for r in results]
        urls = [o.url for o in req_objs]
        self.assertIn(get_url("/api/v1/test/path/val2"), urls)
        self.assertIn(get_url("/api/v1/val/path/test"), urls)
        self.assertEqual(2, len(results))

    def test_post_fuzz_req_json_vars(self):
        """Test fuzz_request with a JSON-like dict."""
        req = post_req(
            "/api/v1/{key:val}/path/{otherkey:val2}", data=test_dict)
        strings = ["test"]
        results = [
            d for d in fuzz_datagen.fuzz_request(req, strings, "data", "ut")
        ]
        req_objs = [r[1] for r in results]
        for d in [o.data for o in req_objs]:
            _dict = json.loads(d)
            self.assertEqual("test", _dict.get("a").get("b"))
            self.assertEqual("e", _dict.get("a").get("d"))
        for url in [o.url for o in req_objs]:
            self.assertEqual(get_url("/api/v1/val/path/val2"), url)
        self.assertEqual(1, len(results))

    def test_get_fuzz_req_params(self):
        """Test fuzz_request against request with params."""
        req = get_req("/api/v1/endpoint", params=test_params_obj)
        strings = ["test", "test2"]
        expected_param_objs = [
            {
                "otherkey": "test",
                "key": "val"
            }, {
                "otherkey": "val2",
                "key": "test"
            }, {
                "otherkey": "test2",
                "key": "val"
            }, {
                "otherkey": "val2",
                "key": "test2"
            }
        ]
        i = 0
        for i, d in enumerate(
                fuzz_datagen.fuzz_request(req, strings, "params", "ut"), 1):
            name, req, fuzz_string, name = d
            self.assertIn(req.params, expected_param_objs)
        self.assertEqual(i, 4)

    def test_var_obj_limits_fuzz(self):
        var_obj = VariableObject(name="no_fuzz_var", val="test", fuzz=False)
        string = "test"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), False)

    def test_var_obj_limits_int(self):
        var_obj = VariableObject(name="int_var", val=1, fuzz_types=["int"])
        string = "test"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), False)
        string = "2"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), True)

    def test_var_obj_limits_ascii(self):
        var_obj = VariableObject(name="ascii_var", val="test",
                                 fuzz_types=["ascii"])
        string = u"\u0124\u0100\u0154\u0100\u004D\u00DF\u00EB"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), False)
        string = "test"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), True)

    def test_var_obj_limits_url(self):
        var_obj = VariableObject(name="url_var", val="test",
                                 fuzz_types=["url"])
        string = "cd /etc; cat passwd"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), False)
        string = "test"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), True)

    def test_var_obj_limits_min_length(self):
        var_obj = VariableObject(name="url_var", val="test",
                                 min_length=5)
        string = "abc"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), False)
        string = "abcde"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), True)

    def test_var_obj_limits_max_length(self):
        var_obj = VariableObject(name="url_var", val="test",
                                 max_length=3)
        string = "abc"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), True)
        string = "abcde"
        self.assertEqual(
            fuzz_datagen._check_var_obj_limits(var_obj, string), False)
