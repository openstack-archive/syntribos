from cafe.drivers.unittest.fixtures import BaseTestFixture

test_table = {}


class TestType(type):
    def __new__(cls, cls_name, cls_parents, cls_attr):
        new_class = super(TestType, cls).__new__(
            cls, cls_name, cls_parents, cls_attr)
        test_name = getattr(new_class, "test_name", None)
        if test_name is not None:
            if test_name in test_table:
                msg = "Test name already used {}".format(test_name)
                raise Exception(msg)
            test_table[test_name] = new_class
        return new_class


class BaseTestCase(BaseTestFixture):
    """
    Base for building new tests
    """
    __metaclass__ = TestType
    test_name = None

    @classmethod
    def get_test_cases(cls, *args, **kwargs):
        yield cls
