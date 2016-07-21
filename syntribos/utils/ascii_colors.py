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
from oslo_config import cfg

CONF = cfg.CONF


def colorize(string, color="nocolor"):
    """A simple method to add ascii colors to the terminal."""

    color_names = ["red", "green", "yellow", "blue"]
    colors = dict(zip(color_names, range(31, 35)))
    colors["nocolor"] = 0  # No Color

    if not CONF.colorize:
        return string
    return "\033[0;{color}m{string}\033[0;m".format(string=string,
                                                    color=colors.setdefault(
                                                        color, 0))
