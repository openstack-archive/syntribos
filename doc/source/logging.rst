Syntribos logging
=================

Syntribos takes advantage of the OpenCafe logging facility. Logs are
found in ``.opencafe/logs/`` Logs are then arranged in directories based
on each Syntribos configuration file, and then by date and time. Each
log filename has an easy to follow naming convention.

::

    $ ls .opencafe/logs/keystone.config/2015-08-18_14_44_04.333088/
    cafe.master.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str1_model1.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str1_model2.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str1_model3.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str2_model1.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str2_model2.log
    syntribos.tests.fuzz.integer_overflow.(domains_post.txt)_(INT_OVERFLOW_BODY)_(integer-overflow.txt)_str2_model3.log

Each log file includes the request details:

::

    ------------
    REQUEST SENT
    ------------
    request method..: POST
    request url.....: https://yourapiendpoint/v3/domains
    request params..:
    request headers.: {'Content-Length': '46', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Accept': 'application/json', 'User-Agent': 'python-requests/2.7.0 CPython/2.7.9 Darwin/11.4.2', 'Host': 'yourapiendpoint', 'X-Auth-Token': u'9b1ed3d1cc69491ab914dcb6ced00440', 'Content-type': 'application/json'}
    request body....: {"domain": {"description": "Domain description","enabled": "-1","name": u'ce9871c4-a0a1-4fbe-88db-f0729b43172c'}}

    2015-08-18 14:44:12,464: DEBUG: cafe.engine.http.client:

and the response:

::

    -----------------
    RESPONSE RECEIVED
    -----------------
    response status..: <Response [406]>
    response time....: 1.32309699059
    response headers.: {'content-length': '112', 'server': 'nginx', 'connection': 'keep-alive', 'date': 'Tue, 18 Aug 2015 19:44:11 GMT', 'content-type': 'application/json; charset=UTF-8'}
    response body....: {"message": "The server could not comply with the request since it is either malformed or otherwise incorrect."}
    -------------------------------------------------------------------------------
    2015-08-18 14:44:12,465: INFO: root: ========================================================
    2015-08-18 14:44:12,465: INFO: root: Test Case....: test_case
    2015-08-18 14:44:12,465: INFO: root: Created At...: 2015-08-18 14:44:11.139070
    2015-08-18 14:44:12,465: INFO: root: No Test description.
    2015-08-18 14:44:12,465: INFO: root: ========================================================
    2015-08-18 14:44:12,465: WARNING: cafe.engine.models.data_interfaces.ConfigParserDataSource: No section: 'fuzz'.  Using default value '200.0' instead
    2015-08-18 14:44:12,465: DEBUG: root: Validate Length:
            Initial request length: 52
            Initial response length: 112
            Request length: 46
            Response length: 112
            Request difference: -6
            Response difference: 0
            Precent difference: 0.0
            Config percent: 200.0

Note the "Validate Length" section at the end. This is used to help
determine whether the test passed or failed. If the *Percent difference*
exceeds the *Config percent* the test has failed. The *Config percent*
is set in ``syntribos/syntribos/tests/fuzz/config.py``. The *Percent
difference* is calculated in
``syntribos/syntribos/tests/fuzz/base_fuzz.py``. Additional validations,
such as looking for SQL strings or stack traces, can be added to
individual tests.

The Logs also contain a summary of data related to the test results
above:

::

    2016-05-19 16:11:52,079: INFO: root: ========================================================
    2016-05-19 16:11:52,079: INFO: root: Test Case......: run_test
    2016-05-19 16:11:52,080: INFO: root: Result.........: Passed
    2016-05-19 16:11:52,080: INFO: root: Start Time.....: 2016-05-19 16:11:52.078475
    2016-05-19 16:11:52,080: INFO: root: Elapsed Time...: 0:00:00.001370
    2016-05-19 16:11:52,080: INFO: root: ========================================================
    2016-05-19 16:11:52,082: INFO: root: ========================================================
    2016-05-19 16:11:52,082: INFO: root: Fixture........: syntribos.tests.fuzz.sql.domains_get.txt_SQL_INJECTION_HEADERS_sql-injection.txt_str19_model2
    2016-05-19 16:11:52,082: INFO: root: Result.........: Passed
    2016-05-19 16:11:52,082: INFO: root: Start Time.....: 2016-05-19 16:11:51.953432
    2016-05-19 16:11:52,083: INFO: root: Elapsed Time...: 0:00:00.129109
    2016-05-19 16:11:52,083: INFO: root: Total Tests....: 1
    2016-05-19 16:11:52,083: INFO: root: Total Passed...: 1
    2016-05-19 16:11:52,083: INFO: root: Total Failed...: 0
    2016-05-19 16:11:52,083: INFO: root: Total Errored..: 0
    2016-05-19 16:11:52,083: INFO: root: ========================================================
