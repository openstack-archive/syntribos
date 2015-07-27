from syntribos.tests.fuzz import base_fuzz


class AllAttacksBody(base_fuzz.BaseFuzzTestCase):
    test_name = "ALL_ATTACKS_BODY"
    test_type = "data"
    data_key = "all-attacks.txt"


class AllAttacksParams(AllAttacksBody):
    test_name = "ALL_ATTACKS_PARAMS"
    test_type = "params"


class AllAttacksHeaders(AllAttacksBody):
    test_name = "ALL_ATTACKS_HEADERS"
    test_type = "headers"


class AllAttacksURL(AllAttacksBody):
    test_name = "ALL_ATTACKS_URL"
    test_type = "url"
    url_var = "FUZZ"
