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
import syntribos.extensions.identity.models.base


class Auth(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(
            self, identity=None, scope=None):
        super(Auth, self).__init__(locals())

    def _obj_to_dict(self):
        return {"auth": self._remove_empty_values({
            "identity": self._get_sub_model(self.identity),
            "scope": self._get_sub_model(self.scope)})}


class Identity(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, token=None, password=None, methods=None):
        super(Identity, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "methods": self.methods or [],
            "password": self._get_sub_model(self.password),
            "token": self._get_sub_model(self.token)})


class Password(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, user=None):
        super(Password, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "user": self._get_sub_model(self.user)})


class User(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, id_=None, password=None, name=None, domain=None):
        super(User, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "id": self.id_,
            "password": self.password,
            "name": self.name,
            "domain": self._get_sub_model(self.domain)})


class Token(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, id_=None):
        super(Token, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({"id": self.id_})


class Scope(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, project=None, domain=None):
        super(Scope, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "project": self._get_sub_model(self.project)})


class Domain(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, name=None, id_=None):
        super(Domain, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "name": self.name,
            "id": self.id_})


class Project(syntribos.extensions.identity.models.base.BaseIdentityModel):

    def __init__(self, name=None, id_=None, domain=None):
        super(Project, self).__init__(locals())

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "name": self.name,
            "id": self.id_,
            "domain": self._get_sub_model(self.domain)})
