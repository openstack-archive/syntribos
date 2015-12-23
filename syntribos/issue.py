"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Issue(object):
    def __init__(self, severity, test="", text="",
                 request=None, response=None, assertions=[]):
        self.test = test
        self.severity = severity
        self.text = text
        self.request = request
        self.response = response
        self.assertions = assertions
        self.failure = False

    def as_dict(self):
        '''Convert the issue to a dict of values for outputting.'''
        out = {
            'test_name': self.test,
            'issue_severity': self.severity,
            'issue_text': self.text,
            'request': self.request_as_dict(self.request),
            'response': self.response_as_dict(self.response)
        }
        return out

    def request_as_dict(self, req):
        return {
            'url': req.path_url,
            'method': req.method,
            'headers': dict(req.headers),
            'body': req.body,
            'cookies': req._cookies.get_dict()
        }

    def response_as_dict(self, res):
        return {
            'status_code': res.status_code,
            'reason': res.reason,
            'url': res.url,
            'headers': dict(res.headers),
            'cookies': res.cookies.get_dict(),
            'text': res.text
        }

    def add_test(self, assertion, *args):
        '''add test

        Assertions will be stored as (assertion, arguments) tuples,
        such as (assertTrue, resp.status != 500) or
        (assertNotIn, line, resp.content)
        '''

        self.assertions.append((assertion,) + args)

    def run_tests(self):
        try:
            for assertion in self.assertions:
                assertion_function = assertion[0]
                condition = assertion[1:]
                assertion_function(*condition)
        except AssertionError as e:
            self.failure = True
            raise e
