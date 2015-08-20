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


class FuzzBehavior(object):
    """
    FuzzBehavior provides the fuzz_data function which yields a test name and
    all iterations of a given piece of data (currently supports dict,
    ElementTree.Element, and basestring formats) with each string provided.
    """

    @classmethod
    def fuzz_data(cls, strings, data, skip_var, name_prefix, string_fuzz_name):
        for str_num, stri in enumerate(strings, 1):
            if isinstance(data, dict):
                model_iter = cls._build_combinations(stri, data, skip_var)
            elif isinstance(data, ElementTree.Element):
                model_iter = cls._build_xml_combinations(stri, data, skip_var)
            elif isinstance(data, basestring):
                model_iter = cls._build_str_combinations(stri, data)
            else:
                raise TypeError("Format not recognized!")
            for model_num, model in enumerate(model_iter, 1):
                name = "{0}str{1}_model{2}".format(
                    name_prefix, str_num, model_num)
                yield (name, model)

    @classmethod
    def _build_str_combinations(cls, name, string, url):
        rep_str = "{{{0}}}".format(name)
        if rep_str in url:
            string = url.format(**{name: string})
            yield string

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
        """
        Uses the copy function to create a merged dictionary without squashing
        the passed in objects
        """
        z = x.copy()
        z.update(y)
        return z

    @classmethod
    def _build_xml_combinations(cls, stri, ele, skip_var):
        if skip_var not in ele.tag:
            if not ele.text or (skip_var not in ele.text):
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
        """
        Returns a copy of the element with the element text replaced by stri
        """
        ret = ele.copy()
        ret.text = stri
        return ret

    @staticmethod
    def _update_attribs(ele, attribs):
        """
        Returns a copy of the element with the attributes replaced by attribs
        """
        ret = ele.copy()
        ret.attrib = attribs
        return ret

    @staticmethod
    def _update_inner_element(ele, list_):
        """
        Returns a copy of the element with the subelements given via list_
        """
        ret = ele.copy()
        for i, v in enumerate(list_):
            ret[i] = v
        return ret
