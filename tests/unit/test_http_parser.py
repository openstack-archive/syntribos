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
import testtools

from syntribos.clients.http import parser
from syntribos.clients.http import VariableObject


endpoint = "http://test.com"


class HTTPParserUnittest(testtools.TestCase):
    parser.meta_vars = {
        "str_var": {"val": "test"},
        "func_var": {
            "type": "function",
            "val":
                "syntribos.extensions.common_utils.client:hmac_it",
            "args": ["test", "key", "md5"]
        },
        "rand_func_var": {
            "type": "function",
            "val":
                "syntribos.extensions.random_data.client:get_uuid"
        },
        "gen_var": {
            "type": "generator",
            "val":
                "syntribos.extensions.random_data.client:get_uuid"
        }
    }

    def test_url_line_parser_vanilla(self):
        """Tests parsing a URL line with simple path."""
        line = "GET / HTTP/1.1"
        method, url, params, version = parser._parse_url_line(line, endpoint)
        self.assertEqual("GET", method)
        self.assertEqual("http://test.com/", url)
        self.assertEqual({}, params)
        self.assertEqual("HTTP/1.1", version)

    def test_url_line_parser_params(self):
        """Tests parsing a URL line with params."""
        line = "GET /path?var=val&var2=val2 HTTP/1.1"
        method, url, params, version = parser._parse_url_line(line, endpoint)
        self.assertEqual("GET", method)
        self.assertEqual("http://test.com/path", url)
        self.assertEqual({"var": "val", "var2": "val2"}, params)
        self.assertEqual("HTTP/1.1", version)

    def test_url_line_parser_invalid_method(self):
        """Tests parsing an invalid HTTP method."""
        line = "DERP /path?var=val&var2=val2 HTTP/1.1"
        self.assertRaises(ValueError, parser._parse_url_line, line, endpoint)

    def test_header_parser_vanilla(self):
        """Tests parsing valid headers."""
        lines = ["Content-Type: application/json", "Accept: application/json"]
        h = {"Content-Type": "application/json", "Accept": "application/json"}
        headers = parser._parse_headers(lines)
        self.assertEqual(h, headers)

    def test_data_parse_vanilla_json(self):
        """Tests parsing valid JSON data."""
        lines = ['{"a": "val", "b": "val2"}']
        dat = parser._parse_data(lines)
        self.assertEqual({"a": "val", "b": "val2"}, dat)

    def test_data_parse_invalid_json(self):
        """Tests parsing invalid JSON data."""
        lines = ['{"a": "val" "b": "val2"}']
        self.assertRaises(TypeError, parser._parse_data, lines)

    def test_data_parse_vanilla_xml(self):
        """Tests parsing valid XML data."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<note type="hi"><to>Tove</to><from>Jani</from></note>'
        ]
        dat = parser._parse_data(lines)
        self.assertEqual("note", dat.tag)
        self.assertEqual({"type": "hi"}, dat.attrib)
        self.assertEqual("to", dat[0].tag)
        self.assertEqual("Tove", dat[0].text)
        self.assertEqual({}, dat[0].attrib)
        self.assertEqual("from", dat[1].tag)
        self.assertEqual("Jani", dat[1].text)
        self.assertEqual({}, dat[1].attrib)

    def test_data_parse_invalid_xml(self):
        """Tests parsing invalid XML data."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<note type="hi"><to>Tove<from></to><from>Jani</from></note>'
        ]
        self.assertRaises(TypeError, parser._parse_data, lines)

    def test_data_parse_vanilla_postdat(self):
        """Tests parsing valid POST (form) data."""
        lines = ["var=val&var2=val2"]
        dat = parser._parse_data(lines)
        self.assertEqual("var=val&var2=val2", dat)

    def test_data_parse_invalid_postdat(self):
        """Tests parsing invalid POST (form) data."""
        lines = ["var = 1, var2 = 2"]
        self.assertRaises(TypeError, parser._parse_data, lines)

    def test_call_external_get_uuid(self):
        """Tests calling 'get_uuid' in URL string."""
        string = 'GET /v1/CALL_EXTERNAL|'
        string += 'syntribos.extensions.random_data.client:get_uuid:[]|'
        parsed_string = parser.call_external_functions(string)
        self.assertRegex(parsed_string, "GET /v1/[a-f0-9]+$")

    def test_call_external_uuid_uuid4(self):
        """Tests calling 'uuid.uuid4()' in URL string."""
        string = 'GET /v1/CALL_EXTERNAL|uuid:uuid4:[]|'
        parsed_string = parser.call_external_functions(string)
        self.assertRegex(parsed_string, "GET /v1/[a-f0-9\-]+$")

    def test_call_external_invalid_module(self):
        """Tests calling invalid module in URL string."""
        string = 'GET /v1/CALL_EXTERNAL|asdfasdfasdf:asdfasdfasdf:[]|'
        self.assertRaises(ImportError, parser.call_external_functions, string)

    def test_call_external_invalid_method(self):
        """Tests calling invalid method in URL string."""
        string = 'GET /v1/CALL_EXTERNAL|uuid:asdfasdfasdf:[]|'
        self.assertRaises(
            AttributeError, parser.call_external_functions, string)

    def test_create_var_obj_str(self):
        var_obj = parser._create_var_obj("str_var")
        self.assertIsInstance(var_obj, VariableObject)
        self.assertEqual("test", var_obj.val)

    def test_create_var_obj_func(self):
        var_obj = parser._create_var_obj("func_var")
        self.assertIsInstance(var_obj, VariableObject)
        self.assertEqual("function", var_obj.var_type)
        self.assertEqual(
            "syntribos.extensions.common_utils.client:hmac_it",
            var_obj.val)
        self.assertEqual(["test", "key", "md5"], var_obj.args)

    def test_create_var_obj_gen(self):
        var_obj = parser._create_var_obj("gen_var")
        self.assertIsInstance(var_obj, VariableObject)
        self.assertEqual("generator", var_obj.var_type)
        self.assertEqual(
            "syntribos.extensions.random_data.client:get_uuid",
            var_obj.val)

    def test_replace_variable_str(self):
        var_obj = parser._create_var_obj("str_var")
        self.assertEqual("test", parser.replace_one_variable(var_obj))

    def test_replace_variable_func(self):
        var_obj = parser._create_var_obj("func_var")
        self.assertEqual("1d4a2743c056e467ff3f09c9af31de7e",
                         parser.replace_one_variable(var_obj))
        self.assertEqual("1d4a2743c056e467ff3f09c9af31de7e",
                         var_obj.function_return_value)

    def test_replace_variable_rand_func(self):
        var_obj = parser._create_var_obj("rand_func_var")
        val_1 = parser.replace_one_variable(var_obj)
        self.assertEqual(val_1, var_obj.function_return_value)
        val_2 = parser.replace_one_variable(var_obj)
        self.assertEqual(val_1, val_2)

    def test_replace_variable_gen(self):
        var_obj = parser._create_var_obj("gen_var")
        val_1 = parser.replace_one_variable(var_obj)
        val_2 = parser.replace_one_variable(var_obj)
        self.assertNotEqual(val_1, val_2)

    def test_replace_dict_variables(self):
        dic = {
            "|str_var|": "|func_var|"
        }
        replaced_dic = parser._replace_dict_variables(dic)
        self.assertIn("test", replaced_dic)
        self.assertIsInstance(dic["test"], VariableObject)
        self.assertEqual(
            dic["test"].val,
            "syntribos.extensions.common_utils.client:hmac_it")
