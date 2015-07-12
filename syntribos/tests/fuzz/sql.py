from syntribos.tests.fuzz import base_fuzz


class SQLInjectionBody(base_fuzz.BaseFuzzTestCase):
    test_name = "SQL_INJECTION_BODY"
    test_type = "data"
    data_key = "sql-injection.txt"


class SQLInjectionParams(SQLInjectionBody):
    test_name = "SQL_INJECTION_PARAMS"
    test_type = "params"


class SQLInjectionHeaders(SQLInjectionBody):
    test_name = "SQL_INJECTION_HEADERS"
    test_type = "headers"


class SQLInjectionURL(SQLInjectionBody):
    test_name = "SQL_INJECTION_URL"
    test_type = "url"
    url_var = "FUZZ"
