from syntribos.tests import base_fuzz


class SQLInjectionBody(base_fuzz.BaseFuzzTestCase):
    test_name = "SQL_INJECTION_BODY"
    test_type = "BODY"
    data_key = "sql-injection.txt"

class SQLInjectionParams(base_fuzz.BaseFuzzTestCase):
    test_name = "SQL_INJECTION_PARAMS"
    test_type = "PARAMS"


class SQLInjectionHeaders(base_fuzz.BaseFuzzTestCase):
    test_name = "SQL_INJECTION_HEADERS"
    test_type = "HEADERS"
