"""
Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""


class Issue(object):
    """Object that encapsulates security vulnerability

    This object is designed to hold the metadata associated with
    an vulnerability, as well as the requests and responses that
    caused the vulnerability to be flagged. Furthermore, holds the
    assertions actually run by the test case
    """
    def __init__(self, severity, test="", text="", confidence="",
                 request=None, response=None):
        self.test = test
        self.severity = severity
        self.confidence = confidence
        self.text = text
        self.request = request
        self.response = response
        self.failure = False

    def as_dict(self):
        '''Convert the issue to a dict of values for outputting.'''
        out = {
            'test_name': self.test,
            'issue_severity': self.severity,
            'issue_text': self.text,
            'request': self.request_as_dict(self.request),
            'response': self.response_as_dict(self.response),
            'issue_confidence': self.confidence
        }
        return out

    def request_as_dict(self, req):
        '''Convert the request object to a dict of values for outputting.'''
        return {
            'url': req.path_url,
            'method': req.method,
            'headers': dict(req.headers),
            'body': req.body,
            'cookies': req._cookies.get_dict()
        }

    def response_as_dict(self, res):
        '''Convert the response object to a dict of values for outputting.'''
        return {
            'status_code': res.status_code,
            'reason': res.reason,
            'url': res.url,
            'headers': dict(res.headers),
            'cookies': res.cookies.get_dict(),
            'text': res.text
        }
