from syntribos.tests.fuzz import base_fuzz


class LDAPInjectionBody(base_fuzz.BaseFuzzTestCase):
    test_name = "LDAP_INJECTION_BODY"
    test_type = "data"
    data_key = "ldap.txt"


class LDAPInjectionParams(LDAPInjectionBody):
    test_name = "LDAP_INJECTION_PARAMS"
    test_type = "params"


class LDAPInjectionHeaders(LDAPInjectionBody):
    test_name = "LDAP_INJECTION_HEADERS"
    test_type = "headers"


class LDAPInjectionURL(LDAPInjectionBody):
    test_name = "LDAP_INJECTION_URL"
    test_type = "url"
    url_var = "FUZZ"
