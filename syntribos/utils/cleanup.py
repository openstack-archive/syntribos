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
# pylint: skip-file
from syntribos.utils.file_utils import delete_dir
import syntribos.utils.remotes


def delete_temps():
    """Deletes all temporary dirs used for saving cached files."""
    remote_dirs = set(syntribos.utils.remotes.remote_dirs)
    temp_dirs = set(syntribos.utils.remotes.temp_dirs)
    [delete_dir(temp_dir) for temp_dir in temp_dirs]    # noqa
    if remote_dirs - temp_dirs:
        print("All downloaded files have been saved to: {}".format(
            ",".join([ele for ele in (remote_dirs - temp_dirs)])))
