from cafe.drivers.unittest.fixtures import BaseTestFixture

test_table = {}


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
        if not isinstance(kwargs, dict):
            raise Exception("kwargs must be a dictionary")
        new_cls = type(new_name, (cls, ), kwargs)
        new_cls.__module__ = cls.__module__
        return new_cls

    def test_case(self):
        pass
