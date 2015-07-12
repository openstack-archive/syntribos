from string import ascii_letters, digits

from cafe.drivers.unittest.fixtures import BaseTestFixture

ALLOWED_CHARS = "().-_{0}{1}".format(ascii_letters, digits)
test_table = {}


def replace_invalid_characters(string, new_char="_"):
    """This functions corrects string so the following is true
    Identifiers (also referred to as names) are described by the
    following lexical definitions:
    identifier ::=  (letter|"_") (letter | digit | "_")*
    letter     ::=  lowercase | uppercase
    lowercase  ::=  "a"..."z"
    uppercase  ::=  "A"..."Z"
    digit      ::=  "0"..."9"
    """
    if not string:
        return string
    for char in set(string) - set(ALLOWED_CHARS):
        string = string.replace(char, new_char)
    if string[0] in digits:
        string = string.replace(string[0], new_char, 1)
    return string


class TestType(type):
    def __new__(cls, cls_name, cls_parents, cls_attr):
        new_class = super(TestType, cls).__new__(
            cls, cls_name, cls_parents, cls_attr)
        test_name = getattr(new_class, "test_name", None)
        if test_name is not None:
            if test_name not in test_table:
                test_table[test_name] = new_class
        return new_class


class BaseTestCase(BaseTestFixture):
    """
    Base for building new tests
    """
    __metaclass__ = TestType
    test_name = None

    @classmethod
    def get_test_cases(cls, filename, file_content):
        yield cls

    @classmethod
    def extend_class(cls, new_name, kwargs):
        new_name = replace_invalid_characters(new_name)
        if not isinstance(kwargs, dict):
            raise Exception("kwargs must be a dictionary")
        new_cls = type(new_name, (cls, ), kwargs)
        new_cls.__module__ = cls.__module__
        return new_cls

    def test_case(self):
        pass
