import json
from xml.etree import ElementTree

from cafe.drivers.unittest.datasets import DatasetList


class DynamicDataGen(DatasetList):
    strings = None

    def __init__(self, name, data, ignore_var):
        for stri in self.strings:
            ctr = 0
            if isinstance(data, dict):
                for dic in self._build_combinations(
                        name, stri, data, ignore_var):
                    self.append_new_dataset(
                        "{0}-{1}-{2}".format(self.test_name, name, ctr), {
                            "model": json.dumps(dic).replace(
                                ignore_var, "")})
                    ctr += 1
            elif isinstance(data, ElementTree.Element):
                for element in self._build_xml_combinations(
                        name, stri, data, ignore_var):
                    self.append_new_dataset(
                        "{0}-{1}-{2}".format(self.test_name, name, ctr), {
                            "model": ElementTree.tostring(element).replace(
                                ignore_var, "")})
                    ctr += 1
            else:
                raise TypeError("Format not recognized!")

    def _build_combinations(self, name, stri, dic, ignore_var):
        for key, val in dic.iteritems():
            if ignore_var in key:
                continue
            elif isinstance(val, dict):
                for ret in self._build_combinations(
                        name, stri, val, ignore_var):
                    yield self._merge_dictionaries(dic, {key: ret})
            elif isinstance(val, list):
                for i, v in enumerate(val):
                    list_ = [_ for _ in val]
                    if isinstance(v, dict):
                        for ret in self._build_combinations(
                                name, stri, v, ignore_var):
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

    def _build_xml_combinations(self, name, stri, ele, ignore_var):
        if ignore_var not in ele.tag:
            if ele.text is not None:
                yield self._update_element(ele, stri)
            for attr in self._build_combinations(
                    name, stri, ele.attrib, ignore_var):
                yield self._update_attribs(ele, attr)
            for i, element in enumerate(list(ele)):
                for ret in self._build_xml_combinations(
                        name, stri, element, ignore_var):
                    list_ = [_ for _ in ele.getchildren()]
                    list_[i] = ret.copy()
                    yield self._update_inner_element(ele, list_)

    def _update_element(self, ele, stri):
        ret = ele.copy()
        ret.text = stri
        return ret

    def _update_attribs(self, ele, attribs):
        ret = ele.copy()
        ret.attrib = attribs
        return ret

    def _update_inner_element(self, ele, list_):
        ret = ele.copy()
        for i, v in enumerate(list_):
            ret[i] = v
        return ret


class ExampleDynamicDataGen(DynamicDataGen):
    strings = ["abc", "def"]
    test_name = "Example"
