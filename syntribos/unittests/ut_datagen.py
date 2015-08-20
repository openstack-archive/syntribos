from xml.etree import ElementTree
import unittest2 as unittest

from syntribos.tests.fuzz.datagen import FuzzBehavior


class FuzzBehaviorUnittest(unittest.TestCase):
    def test_fuzz_data_dict(self):
        data = {"a": {"b": "c", "ACTION_FIELD:d": "e"}}
        strings = ["test"]

        for i, d in enumerate(FuzzBehavior.fuzz_data(
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

        for i, d in enumerate(FuzzBehavior.fuzz_data(
                strings, data, "ACTION_FIELD:", "unittest"), 1):
            name, model = d
            assert model[1].tag == "ACTION_FIELD:d" and model[1].text == "e"
            assert model.text == "test" or model[0].text == "test"
            assert name == "unitteststr1_model{0}".format(i)
