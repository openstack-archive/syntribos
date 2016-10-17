Syntribos logging
=================

Syntribos generates results log and debug logs. Result logs are the representation of results
(collection of issues) from a given syntribos run.

Results Log
____________

The result format has the keys "failures" (for tests that failed, indicating a possible security
vulnerability) and "errors" (for tests that encountered some kind of unhandled exception, such
as a connection error).

An example failure object is seen below:

::

    {
       "defect_type": "xss_strings",
       "description": "The string(s): '[\"<STYLE>@import'http://xss.rocks/xss.css';</STYLE>\"]',
       known to be commonly returned after a successful XSS attack, have been found in the
       response. This could indicate a vulnerability to XSS attacks.",
       "failure_id": 33,
       "instances": [
          {
            "confidence": "LOW",
            "param": {
              "location": "data",
              "method": "POST",
              "type": null,
              "variables": [
                "type",
                "details/name",
              ]
          },
          "severity": "LOW",
          "signals": {
             "diff_signals": [
               "LENGTH_DIFF_OVER"
             ],
             "init_signals": [
               "HTTP_CONTENT_TYPE_JSON",
               "HTTP_STATUS_CODE_2XX_201"
             ],
             "test_signals": [
               "FAILURE_KEYS_PRESENT",
               "HTTP_CONTENT_TYPE_JSON",
               "HTTP_STATUS_CODE_2XX_201",
             ]
          },
          "strings": [
            "<STYLE>@import'http://xss.rocks/xss.css';</STYLE>"
             ]
          }
       ],
       "url": "127.0.0.1/test"
    }


Errors take the form:

:: 

    ERROR:
    {
      "error": "Traceback (most recent call last):\n  File \"/Users/test/syntribos/tests/fuzz/base_fuzz.py\",
       line 58, in tearDownClass\n    super(BaseFuzzTestCase, cls).tearDownClass()\n
       File \"/Users/test/syntribos/tests/base.py\", line 166, in tearDownClass\n
       raise sig.data[\"exception\"]\nReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8080):
       Read timed out. (read timeout=10)\n",
       "test": "tearDownClass (syntribos.tests.fuzz.sql.image_data_image_data_get.template_SQL_INJECTION_HEADERS_sql-injection.txt_str21_model1)"
    }


Debug Logs
__________

Debug logs include details about HTTP requests and responses, and any debug information like errors
and warnings across the project. They are found in ``.syntribos/logs/``.
Debug logs are arranged in directories based on date and time, and then
in files according to the templates.

::

    $ ls .syntribos/logs/
    2016-09-15_11:06:37.198412 2016-09-16_10:11:37.834892 2016-09-16_13:31:36.362584
    2016-09-15_11:34:33.271606 2016-09-16_10:38:55.820827 2016-09-16_13:36:43.151048
    2016-09-15_11:41:53.859970 2016-09-16_10:39:50.501820 2016-09-16_13:40:23.203920
    2016-09-15_17:50:54.787628 2016-09-16_10:43:36.158882 2016-09-21_14:07:33.293527
    2016-09-16_10:00:49.615684 2016-09-16_13:30:51.624665 2016-09-21_14:08:26.682639

::

    $ ls .syntribos/logs/2016-09-16_13:31:36.362584
    API_Versions::list_versions_template.log
    API_Versions::show_api_details_template.log
    availability_zones::get_availablilty_zone_detail_template.log
    availability_zones::get_availablilty_zone_template.log
    cells::delete_os_cells_template.log
    cells::get_os_cells_capacities_template.log
    cells::get_os_cells_data_template.log

Each log file includes some essential debugging information like the string representation
of the request object, signals and checks used for tests.

The request:

::

    ------------
    REQUEST SENT
    ------------
    request method.......: PUT
    request url..........: http://127.0.0.1/api
    request params.......:
    request headers size.: 7
    request headers......: {'Content-Length': '0', 'Accept-Encoding': 'gzip, deflate',
    'Accept': 'application/json',
    'X-Auth-Token': <uuid>, 'Connection': 'keep-alive',
    'User-Agent': 'python-requests/2.11.1', 'content-type': 'application/xml'}
    request body size....: 0
    request body.........: None

The response:

::

    -----------------
    RESPONSE RECEIVED
    -----------------
    response status..: <Response [415]>
    response headers.: {'Content-Length': '70',
    'X-Compute-Request-Id': <random id>,
    'Vary': 'OpenStack-API-Version, X-OpenStack-Nova-API-Version',
    'Openstack-Api-Version': 'compute 2.1', 'Connection': 'close',
    'X-Openstack-Nova-Api-Version': '2.1', 'Date': 'Fri, 16 Sep 2016 14:15:27 GMT',
    'Content-Type': 'application/json; charset=UTF-8'}
    response time....: 0.036277
    response size....: 70
    response body....: {"badMediaType": {"message": "Unsupported Content-Type", "code": 415}}
    -------------------------------------------------------------------------------
    [2590]  :  XSS_BODY
    (<syntribos.clients.http.client.SynHTTPClient object at 0x102c65f10>, 'PUT',
    'http://127.0.0.1/api')
    {'headers': {'Accept': 'application/json', 'X-Auth-Token': <uuid> },
    'params': {}, 'sanitize': False, 'data': '', 'requestslib_kwargs': {'timeout': 10}}
    Starting new HTTP connection (1): 127.0.0.1
    "PUT http://127.0.0.1/api HTTP/1.1" 501 93

And the signals captured:

::

    Signals: ['HTTP_STATUS_CODE_4XX_400', 'HTTP_CONTENT_TYPE_JSON']
    Checks used: ['HTTP_STATUS_CODE', 'HTTP_CONTENT_TYPE']

Debug logs are sanitized to prevent storing secrets to log files.
Passwords and other sensitive information are masked with astericks using a slightly modified
version of `oslo_utils.strutils.mask_password <http://docs.openstack.org/developer/oslo.utils/api/strutils.html#oslo_utils.strutils.mask_password_>`

Debug logs also includes body compression, wherein long fuzz strings are compressed before being
written to the logs. The threshold to start data compression is set at 512 characters.
Compression can be turned off by setting the http_request_compression to ``False`` under logging
section in the config file.
