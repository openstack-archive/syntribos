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
import os

import mock
import six
import testtools

import syntribos.config
import syntribos.utils.env as ENV

syntribos.config.register_opts()


class EnvUtilsUnittest(testtools.TestCase):

    def test_get_user_home_root(self):
        """Check that we get something reasonable from get_user_home_root."""
        home_root = ENV.get_user_home_root()
        home_dir = os.path.abspath(os.path.join(home_root, ".."))
        self.assertIsInstance(home_root, six.string_types)
        self.assertIsNot("", home_root)
        self.assertIsNot("/", home_root)
        self.assertTrue(os.path.isdir(home_dir))

    def test_get_syntribos_root(self):
        """Check that we get something reasonable from get_syntribos_root."""
        root = ENV.get_syntribos_root()
        root_parent = os.path.abspath(os.path.join(root, ".."))
        self.assertIsInstance(root, six.string_types)
        self.assertIsNot("", root)
        self.assertIsNot("/", root)
        self.assertTrue(os.path.isdir(root_parent))

    def test_get_syntribos_path(self):
        """Check that we get something reasonable from get_syntribos_path."""
        root = ENV.get_syntribos_root()
        self.assertIsInstance(root, six.string_types)
        root_parent = os.path.abspath(os.path.join(root, ".."))
        path_parent = ENV.get_syntribos_path("..")
        self.assertEqual(root_parent, path_parent)

    def test_get_log_dir_name(self):
        """Check that we get something reasonable from get_log_dir_name."""
        log_dir = ENV.get_log_dir_name()
        self.assertIsInstance(log_dir, six.string_types)
        root_parent = os.path.abspath(os.path.join(log_dir, "..", ".."))
        self.assertIsInstance(log_dir, six.string_types)
        self.assertIsNot("", log_dir)
        self.assertIsNot("/", log_dir)
        self.assertTrue(os.path.isdir(root_parent))

    @mock.patch("os.makedirs")
    def test_create_env_dirs(self, makedirs):
        ENV.create_env_dirs(ENV.get_syntribos_root())
