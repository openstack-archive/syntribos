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
from __future__ import division
from __future__ import unicode_literals
from math import ceil
import sys

from oslo_config import cfg

import syntribos

CONF = cfg.CONF


def print_symbol():
    """Syntribos radiation symbol."""
    symbol = """               Syntribos
                xxxxxxx
           x xxxxxxxxxxxxx x
        x     xxxxxxxxxxx     x
               xxxxxxxxx
     x          xxxxxxx          x
                 xxxxx
    x             xxx             x
                   x
   xxxxxxxxxxxxxxx   xxxxxxxxxxxxxxx
    xxxxxxxxxxxxx     xxxxxxxxxxxxx
     xxxxxxxxxxx       xxxxxxxxxxx
      xxxxxxxxx         xxxxxxxxx
        xxxxxx           xxxxxx
          xxx             xxx
              x         x
                   x
      === Automated API Scanning  ==="""
    print(syntribos.SEP)
    print(symbol)
    print(syntribos.SEP)


def colorize(string, color="nocolor"):
    """Method to add ascii colors to the terminal."""

    color_names = ["red", "green", "yellow", "blue"]
    colors = dict(list(zip(color_names, list(range(31, 35)))))
    colors["nocolor"] = 0  # No Color

    if not CONF.colorize:
        return string
    return "\033[0;{color}m{string}\033[0;m".format(string=string,
                                                    color=colors.setdefault(
                                                        color, 0))


class ProgressBar(object):
    """A simple progressBar.

    A simple generic progress bar like many others.
    :param int total_len: total_len value, when progress is 100 %
    :param int width: width of the progress bar
    :param str fill_char: character to show progress
    :param str empty_char: character to show empty part
    :param str message: string to be part of the progress bar
    """

    def __init__(self, total_len=30, width=23, fill_char="#", empty_char="-",
                 message=""):
        self.width = width
        self.total_len = total_len
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.message = message
        self.present_level = 0

    def increment(self, inc_level=1):
        """Method to increment the progress.

        :param int inc_level: level of increment
        :returns: None
        """
        if self.total_len > self.present_level + inc_level:
            self.present_level += inc_level
        else:
            self.present_level = self.total_len

    def format_bar(self):
        """Method to format the progress bar.

        This method appends the message string and the progress bar,
        also calculates the percentage of progress and appends it
        to the formatted progress bar

        :returns: formatted progress bar string
        """
        bar_width = int(ceil(self.present_level / self.total_len * self.width))
        empty_char = self.empty_char * (self.width - bar_width)
        fill_char = self.fill_char * bar_width
        percentage = int(self.present_level / self.total_len * 100)
        return "{message}\t\t|{fill_char}{empty_char}|  {percentage} %".format(
            message=self.message, fill_char=fill_char,
            empty_char=empty_char, percentage=percentage)

    def print_bar(self):
        """As the method says, prints the bar to standard out."""
        sys.stdout.write("\r")
        sys.stdout.write((self.format_bar()))
        sys.stdout.flush()
