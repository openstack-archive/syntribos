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
import uuid
import xml.etree.ElementTree as ElementTree

import six
import testtools

from syntribos.clients.http.parser import _iterators
from syntribos.clients.http.parser import RequestHelperMixin as rhm
from syntribos.clients.http.parser import RequestObject as ro

endpoint = "http://test.com"
action_field = "ACTION_FIELD:"


def get_fake_generator():
    for i in range(2):
        yield str(i)


def get_url(path):
    """Helper method to append endpoint and slash if necessary."""
    return "{endpoint}{sep}{path}".format(
        endpoint=endpoint,
        sep="/" if not path.startswith("/") else "",
        path=path)


def create_default_req(*args, **kwargs):
    if not kwargs.get("action_field"):
        kwargs["action_field"] = action_field
    if not kwargs.get("headers"):
        kwargs["headers"] = {"Content-Type": "application/json"}
    return ro(*args, **kwargs)


def get_req(path, *args, **kwargs):
    return create_default_req("GET", get_url(path), *args, **kwargs)


def post_req(path, *args, **kwargs):
    return create_default_req("POST", get_url(path), *args, **kwargs)


class HTTPModelsUnittest(testtools.TestCase):
    def test_remove_braces_named(self):
        """Tests RequestHelperMixin._remove_braces() with a named var."""
        res = rhm._remove_braces("{id:123}")
        self.assertEqual("id:123", res)

    def test_remove_braces_double_braces(self):
        """Tests RequestHelperMixin._remove_braces() with double braces."""
        res = rhm._remove_braces("{{id:123}}")
        self.assertEqual("{id:123}", res)

    def test_remove_braces_multi_vars(self):
        """Tests RequestHelperMixin._remove_braces() with multiple vars."""
        res = rhm._remove_braces("{id:123}/user/{user_id:1234}")
        self.assertEqual("id:123/user/user_id:1234", res)

    def test_remove_attrib_then_braces(self):
        """Tests RHM._remove_braces() and RHM._remove_attr_names()."""
        res = rhm._remove_attr_names("{id:123}/user/{user_id:1234}")
        self.assertEqual("{123}/user/{1234}", res)
        res = rhm._remove_braces(res)
        self.assertEqual("123/user/1234", res)

    def test_string_dat_valid_dict(self):
        """Tests RHM._string_data() with a valid dict."""
        _dict = {"a": "val", "b": "val2"}
        res = rhm._string_data(_dict)
        j_dat = json.loads(res)
        self.assertEqual(_dict, j_dat)

    def test_string_dat_invalid_dict(self):
        """Tests RHM._string_data() with an unserializable dict."""
        _dict = {"a": set([1, 2, 3])}
        self.assertRaises(TypeError, rhm._string_data, _dict)

    def test_string_dat_valid_xml(self):
        """Tests RHM._string_data() with a valid XML object."""
        a = ElementTree.Element("a")
        b = ElementTree.Element("b")
        b.text = "hey"
        a.append(b)
        res = rhm._string_data(a)
        self.assertEqual("<a><b>hey</b></a>", res)

    def test_string_dat_valid_xml_w_attrs(self):
        """Tests RHM._string_data() with a valid XML object."""
        a = ElementTree.Element("a")
        a.attrib = {"key": "val"}
        b = ElementTree.Element("b")
        b.text = "hey"
        a.append(b)
        res = rhm._string_data(a)
        self.assertEqual('<a key="val"><b>hey</b></a>', res)

    def test_run_iters_dict_w_multiple_list(self):
        """Tests RHM._run_iters() w/ dict containing 2 lists."""
        _dict = {
            "a": ["ACTION_FIELD:var", "var2", "var3", ["ACTION_FIELD:var4"]]
        }
        res = rhm._run_iters(_dict, action_field)
        self.assertEqual(["var", "var2", "var3", ["var4"]], res.get("a"))

    def test_run_iters_dict_w_list_w_dict(self):
        """Tests RHM._run_iters() w/ dict w/ a list containing a dict."""
        _dict = {"a": [{"ACTION_FIELD:b": "c"}]}
        res = rhm._run_iters(_dict, action_field)
        self.assertEqual({"b": "c"}, res.get("a")[0])

    def test_run_iters_xml(self):
        """Tests RHM._run_iters() w/ dict containing 2 lists."""
        root = ElementTree.Element("root")
        a = ElementTree.Element("a")
        a.attrib = {"ACTION_FIELD:attrib": "val"}
        a.text = "ACTION_FIELD:var"
        root.append(a)
        res = rhm._run_iters(root, action_field)
        res_text = ElementTree.tostring(res)
        if not six.PY2:
            res_text = res_text.decode("utf-8")
        self.assertEqual('<root><a attrib="val">var</a></root>', res_text)

    def test_run_iters_global_iterators(self):
        """Tests _replace_iter by modifying _iterators global object."""
        u = str(uuid.uuid4()).replace("-", "")
        _iterators[u] = get_fake_generator()
        _str = "/v1/{0}/test".format(u)
        res = rhm._run_iters(_str, action_field)
        self.assertEqual("/v1/{0}/test".format(0), res)

    def test_prepare_req_action_field_dat(self):
        """Tests RHM.prepare_request() with an ACTION_FIELD var in body."""
        r = get_req("/", data={"ACTION_FIELD:var": 1234})
        prep = r.get_prepared_copy()
        j_dat = json.loads(prep.data)
        self.assertEqual(1234, j_dat.get("var"))

    def test_prepare_req_action_field_param(self):
        """Tests RHM.prepare_request() with an ACTION_FIELD param."""
        params = {"ACTION_FIELD:var": 1234}
        r = get_req("/", params=params)
        prep = r.get_prepared_copy()
        self.assertEqual(1234, prep.params.get("var"))

    def test_prepare_req_named_var_url(self):
        """Tests RHM.prepare_request() with a named variable in URL."""
        r = get_req("/{id:123}")
        prep = r.get_prepared_copy()
        self.assertEqual("http://test.com/123", prep.url)

    def test_prepare_req_action_field_url(self):
        """Tests RHM.prepare_request() with an ACTION_FIELD in URL."""
        r = get_req("/{ACTION_FIELD:id:123}")
        prep = r.get_prepared_copy()
        self.assertEqual("http://test.com/123", prep.url)
