from syntribos.tests.base import BaseTest, BaseTestConfig


class SQLInjectionBody(BaseTest):
    test_name = "SQL_INJECTION_BODY"
    test_type = "BODY"
    filename = "sql-injection.txt"
    config = BaseTestConfig(section_name=test_name)


class SQLInjectionParams(SQLInjectionBody):
    test_name = "SQL_INJECTION_PARAMS"
    test_type = "PARAMS"


class SQLInjectionHeaders(SQLInjectionBody):
    test_name = "SQL_INJECTION_HEADERS"
    test_type = "HEADERS"


class SQLInjectionURL(SQLInjectionBody):
    test_name = "SQL_INJECTION_URL"
    test_type = "URL"
