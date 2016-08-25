# Copyright 2016 Intel
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
import testtools

from syntribos.clients.http import debug_logger


class TestDebugLogger(testtools.TestCase):

    def test_sanitize_dicts(self):
        content = {"creds": {"password": "12345"}, "sl.no": 1}
        sanitized_content = {"creds": {"password": "****"}, "sl.no": 1}
        self.assertEqual(sanitized_content,
                         debug_logger.sanitize_secrets(content))

    def test_sanitize_strings(self):
        content = "password = 12344"
        sanitized_content = "password = ****"
        self.assertEqual(sanitized_content,
                         debug_logger.sanitize_secrets(content))

    def test_compress(self):
        content = "Sample data for compression"
        encoded_content = "eJwLTswtyElVSEksSVRIyy9SSM7PLShKLS7OzM8DAIvJClY="
        compressed_content = debug_logger.compress(content, threshold=10)
        compressed_data = ("******Content compressed by Syntribos.******\n"
                           "First fifty characters of the content:\n"
                           "       {data}\n       "
                           "Base64 encoded compressed content:\n"
                           "       {compressed}\n      "
                           "******End of compressed content.******\n").format(
                               data=content, compressed=encoded_content)
        self.assertEqual(compressed_content, compressed_data)
