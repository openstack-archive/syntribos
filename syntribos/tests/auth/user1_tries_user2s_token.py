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
from syntribos.tests.auth import base_auth


class AuthWithSomeoneElsesToken(base_auth.BaseAuthTestCase):

    """AuthWithSomeoneElsesToken Class

    This is just a specialization of the base auth test class
    which supplies the test name and type.
    """
    test_name = "AUTH_WITH_SOMEONE_ELSE_TOKEN"
    test_type = "headers"
