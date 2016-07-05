# Copyright 2016 Rackspace
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
from oslo_config import cfg

from syntribos.clients.http.models import RequestHelperMixin
from syntribos.clients.http.models import RequestObject
from syntribos.clients.http import parser

CONF = cfg.CONF


class AuthMixin(object):

    """AuthMixin Class

    AuthBehavior provides utility methods to manipulate data before
    a request object is created.
    """

    @staticmethod
    def remove_braces(string):
        return string.replace("}", "").replace("{", "")


class AuthRequest(RequestObject, AuthMixin, RequestHelperMixin):

    """AuthRequest Class

    This class specializes the generic RequestObject to
    create an auth test specific class.
    """

    def prepare_request(self, auth_type=None):
        super(AuthRequest, self).prepare_request()
        if auth_type != "url":
            self.url = self.remove_braces(self.url)
        user_id = CONF.user.project
        self.url = self.url.replace('USER_ID', user_id)


class AuthParser(parser):

    """AuthParser Class

    This class is a container class to hold
    an auth request object type.
    """

    request_model_type = AuthRequest
