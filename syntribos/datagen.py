import json
from xml.etree import ElementTree

from cafe.engine.behaviors import BaseBehavior


class FuzzBehavior(BaseBehavior):
    @classmethod
    def fuzz_body(cls, strings, data, skip_var, name):
        for str_num, stri in enumerate(strings, 1):
            if isinstance(data, dict):
                model_iter = cls._build_combinations(stri, data, skip_var)
            elif isinstance(data, ElementTree.Element):
                model_iter = cls._build_xml_combinations(stri, data, skip_var)
            else:
                raise TypeError("Format not recognized!")
            for model_num, model in enumerate(model_iter, 1):
                name = "{0}_str{1}_model{2}".format(name, str_num, model_num)
                if isinstance(dict):
                    string = json.dumps(model)
                else:
                    string = ElementTree.tostring(model)
                string = string.replace(skip_var, "")
                yield (name, string)

    @classmethod
    def _build_combinations(cls, stri, dic, skip_var):
        for key, val in dic.iteritems():
            if skip_var in key:
                continue
            elif isinstance(val, dict):
                for ret in cls._build_combinations(stri, val, skip_var):
                    yield cls._merge_dictionaries(dic, {key: ret})
            elif isinstance(val, list):
                for i, v in enumerate(val):
                    list_ = [_ for _ in val]
                    if isinstance(v, dict):
                        for ret in cls._build_combinations(stri, v, skip_var):
                            list_[i] = ret.copy()
                            yield cls._merge_dictionaries(dic, {key: list_})
                    else:
                        list_[i] = stri
                        yield cls._merge_dictionaries(dic, {key: list_})
            else:
                yield cls._merge_dictionaries(dic, {key: stri})

    @staticmethod
    def _merge_dictionaries(x, y):
        z = x.copy()
        z.update(y)
        return z

    @classmethod
    def _build_xml_combinations(cls, stri, ele, skip_var):
        if skip_var not in ele.tag:
            if ele.text is not None:
                yield cls._update_element(ele, stri)
            for attr in cls._build_combinations(stri, ele.attrib, skip_var):
                yield cls._update_attribs(ele, attr)
            for i, element in enumerate(list(ele)):
                for ret in cls._build_xml_combinations(
                        stri, element, skip_var):
                    list_ = [_ for _ in ele.getchildren()]
                    list_[i] = ret.copy()
                    yield cls._update_inner_element(ele, list_)

    @staticmethod
    def _update_element(ele, stri):
        ret = ele.copy()
        ret.text = stri
        return ret

    @staticmethod
    def _update_attribs(ele, attribs):
        ret = ele.copy()
        ret.attrib = attribs
        return ret

    @staticmethod
    def _update_inner_element(ele, list_):
        ret = ele.copy()
        for i, v in enumerate(list_):
            ret[i] = v
        return ret
