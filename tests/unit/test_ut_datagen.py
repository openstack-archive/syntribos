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
from xml.etree import ElementTree
import unittest2 as unittest

from syntribos.tests.fuzz.datagen import FuzzMixin


class FuzzMixinUnittest(unittest.TestCase):
    def test_fuzz_data_dict(self):
        data = {"a": {"b": "c", "ACTION_FIELD:d": "e"}}
        strings = ["test"]

        for i, d in enumerate(FuzzMixin._fuzz_data(
                strings, data, "ACTION_FIELD:", "unittest"), 1):
            name, model = d
            assert model.get("a").get("ACTION_FIELD:d") == "e"
            assert model.get("a").get("b") == "test"
            assert name == "unitteststr1_model{0}".format(i)

    def test_fuzz_data_xml(self):
        data = ElementTree.Element("a")
        sub_ele = ElementTree.Element("b")
        sub_ele.text = "c"
        sub_ele2 = ElementTree.Element("ACTION_FIELD:d")
        sub_ele2.text = "e"
        data.append(sub_ele)
        data.append(sub_ele2)
        strings = ["test"]

        for i, d in enumerate(FuzzMixin._fuzz_data(
                strings, data, "ACTION_FIELD:", "unittest"), 1):
            name, model = d
            assert model[1].tag == "ACTION_FIELD:d" and model[1].text == "e"
            assert model.text == "test" or model[0].text == "test"
            assert name == "unitteststr1_model{0}".format(i)

    def test_fuzz_data_string(self):
        data = "THIS_IS_MY_STRING_THERE_ARE_MANY_LIKE_IT_BUT_THIS_IS_MINE/{ST}"
        strings = ["test"]

        for i, d in enumerate(FuzzMixin._fuzz_data(
                strings, data, "ACTION_FIELD:", "unittest"), 1):
            name, model = d
            assert "test" in model
            assert name == "unitteststr1_model{0}".format(i)
