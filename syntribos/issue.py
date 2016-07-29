# Copyright 2015 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Issue(object):

    """Object that encapsulates a security vulnerability

    This object is designed to hold the metadata associated with
    a vulnerability.

    :ivar defect_type: The type of vulnerability that Syntribos believes it has
        found. This may be something like 500 error or DoS, regardless of what
        the Test Type is.
    :ivar severity: "Low", "Medium", or "High", depending on the defect
    :ivar description: Description of the defect
    :ivar confidence: The confidence of the defect
    :ivar request: The request object sent that generated this defect
    :ivar response: The response object returned after sending the request
    :ivar target: A hostname/IP/etc. to be tested
    :ivar path: A specific REST API method, i.e. a URL path associated with a
        Target.
    :ivar test_type: The type of vulnerability that is being tested for. This
        is not necessarily the same as the Defect Type, which may be something
        like 500 error or DoS.
    :ivar content_type: The content-type of the unmodified request
    :ivar impacted_parameter: For fuzz tests only, a
        :class:`syntribos.tests.fuzz.base_fuzz.ImpactedParameter` that holds
        data about what part of the request was affected by the fuzz test.
    """

    def __init__(self, defect_type, severity, description, confidence,
                 request=None, response=None, impacted_parameter=None,
                 init_signals=[], test_signals=[], diff_signals=[]):
        self.defect_type = defect_type
        self.severity = severity
        self.description = description
        self.confidence = confidence
        self.request = request
        self.response = response
        self.impacted_parameter = None
        self.init_signals = init_signals
        self.test_signals = test_signals
        self.diff_signals = diff_signals

    def as_dict(self):
        """Convert the issue to a dict of values for outputting.

        :rtype: `dict`
        :returns: dictionary of issue data
        """
        out = {
            'issue_target': self.target,
            'issue_path': self.path,
            'issue_defect_type': self.defect_type,
            'issue_test_type': self.test_type,
            'issue_severity': self.severity,
            'issue_description': self.text,
            'issue_confidence': self.confidence
        }

        if self.impacted_parameter:
            out['impacted_parameter'] = self.impacted_parameter.as_dict()

        return out

    def get_details(self):
        """Returns the most relevant information needed for output.

        :rtype: `dict`
        :returns: dictionary of issue details
        """
        return {
            'description': self.text,
            'confidence': self.confidence,
            'severity': self.severity
        }

    def request_as_dict(self, req):
        """Convert the request object to a dict of values for outputting.

        :param req: The request object
        :rtype: `dict`
        :returns: dictionary of HTTP request data
        """
        return {
            'url': req.path_url,
            'method': req.method,
            'headers': dict(req.headers),
            'body': req.body,
            'cookies': req._cookies.get_dict()
        }

    def response_as_dict(self, res):
        """Convert the response object to a dict of values for outputting.

        :param res: The result object
        :rtype: `dict`
        :returns: dictionary of HTTP response data
        """
        return {
            'status_code': res.status_code,
            'reason': res.reason,
            'url': res.url,
            'headers': dict(res.headers),
            'cookies': res.cookies.get_dict(),
            'text': res.text
        }
