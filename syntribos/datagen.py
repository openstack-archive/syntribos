import json
from xml.etree import ElementTree

from cafe.drivers.unittest.datasets import DatasetList


class DynamicDataGen(DatasetList):
    strings = None

    def __init__(self, name, data):
        for stri in self.strings:
            ctr = 0
            if isinstance(data, dict):
                for dic in self._build_combinations(name, stri, data):
                    self.append_new_dataset(
                        "{0}-{1}-{2}".format(self.test_name, name, ctr), {
                            "model": json.dumps(dic)})
                    ctr += 1
            elif isinstance(data, ElementTree.Element):
                for element in self._build_xml_combinations(name, stri, data):
                    self.append_new_dataset(
                        "{0}-{1}-{2}".format(self.test_name, name, ctr), {
                            "model": ElementTree.tostring(element)})
                    ctr += 1
            else:
                raise TypeError("Format not recognized!")

    def _build_combinations(self, name, stri, dic):
        for key, val in dic.iteritems():
            if isinstance(val, dict):
                for ret in self._build_combinations(name, stri, val):
                    yield self._merge_dictionaries(dic, {key: ret})
            elif isinstance(val, list):
                for i, v in enumerate(val):
                    list_ = [_ for _ in val]
                    if isinstance(v, dict):
                        for ret in self._build_combinations(name, stri, v):
                            list_[i] = ret.copy()
                            yield self._merge_dictionaries(dic, {key: list_})
                    else:
                        list_[i] = stri
                        yield self._merge_dictionaries(dic, {key: list_})
            else:
                yield self._merge_dictionaries(dic, {key: stri})

    def _merge_dictionaries(self, x, y):
        z = x.copy()
        z.update(y)
        return z

    def _build_xml_combinations(self, name, stri, ele):
        if ele.text is not None:
            yield self._update_element(ele, stri)
        for i, element in enumerate(ele.getchildren()):
            for ret in self._build_xml_combinations(name, stri, element):
                list_ = [_ for _ in ele.getchildren()]
                list_[i] = ret.copy()
                yield self._update_inner_element(ele, list_)

    def _update_element(self, ele, stri):
        ret = ele.copy()
        ret.text = stri
        return ret

    def _update_inner_element(self, ele, list_):
        ret = ele.copy()
        for i, v in enumerate(list_):
            ret[i] = v
        return ret


class ExampleDynamicDataGen(DynamicDataGen):
    strings = ["abc", "def"]
    test_name = "Example"
