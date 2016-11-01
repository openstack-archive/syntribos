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

from syntribos.extensions.common_utils import client


class TestStackTrace(testtools.TestCase):
    def test_hash_it(self):
        hash_val = client.hash_it("test")
        self.assertEqual(hash_val, ("9f86d081884c7d659a2feaa0c"
                                    "55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"))

    def test_hash_it_md5(self):
        hash_val = client.hash_it("test", "md5")
        self.assertEqual(hash_val, "098f6bcd4621d373cade4e832627b4f6")

    def test_hmac_it(self):
        hmac_val = client.hmac_it("test", "key")
        self.assertEqual(hmac_val, ("02afb56304902c656fcb737cd"
                                    "d03de6205bb6d401da2812efd9b2d36a08af159"))

    def test_hmac_it_md5(self):
        hmac_val = client.hmac_it("test", "key", "md5")
        self.assertEqual(hmac_val, "1d4a2743c056e467ff3f09c9af31de7e")

    def test_url_encode(self):
        u_encode = client.url_encode("https://example.com/")
        self.assertEqual(u_encode, "https%3A%2F%2Fexample.com%2F")

    def test_base64_encode(self):
        b_encode = client.base64_encode("test")
        self.assertEqual(b_encode, b"dGVzdA==")

    def test_epoch_time(self):
        self.assertTrue(type(client.epoch_time()), float)

    def test_utc_datetime(self):
        self.assertTrue(type(client.utc_datetime()), str)
