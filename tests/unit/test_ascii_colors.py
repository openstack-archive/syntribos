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

from syntribos.utils.cli import colorize
from syntribos.utils.cli import CONF


class TestColorize(testtools.TestCase):

    def test_colorize(self):
        CONF.colorize = True
        string = "color this string"
        colors = {"red": 31,
                  "green": 32,
                  "yellow": 33,
                  "blue": 34,
                  "nocolor": 0}
        for color in colors:
            self.assertEqual(
                "\033[0;{clr}m{string}\033[0;m".format(
                    string=string, clr=colors[color]),
                colorize(string, color))

    def test_no_colorize(self):
        CONF.colorize = False
        string = "No color"
        self.assertEqual(string, colorize(string))
