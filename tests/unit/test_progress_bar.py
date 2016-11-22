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

from syntribos.utils.cli import ProgressBar


class TestProgressBar(testtools.TestCase):

    def test_pb(self):
        pb = ProgressBar(fill_char="#", message="Test")
        self.assertEqual(pb.total_len, 30)
        self.assertEqual(pb.width, 23)
        self.assertEqual(pb.fill_char, "#")
        self.assertEqual(pb.message, "Test")

    def test_increment(self):
        pb = ProgressBar()
        pb.increment(10)
        self.assertEqual(10, pb.present_level)
        pb.increment(20)
        self.assertEqual(pb.present_level, pb.total_len)

    def test_format_bar(self):
        pb = ProgressBar(total_len=5, width=5, fill_char="#", message="Test")
        pb.increment()  # increments progress bar by 1
        self.assertEqual(u"Test\t\t|#----|  20 %", pb.format_bar())

    def test_print_bar(self):
        pb = ProgressBar(total_len=5, width=5, fill_char="#", message="Test")
        pb.increment()  # increments progress bar by 1
        self.assertIsNone(pb.print_bar())
