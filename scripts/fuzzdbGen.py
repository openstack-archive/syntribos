"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys

fuzzdb_path = "{fuzzdb_dir}/attack-payloads".format(
    fuzzdb_dir=sys.argv[1])
syntribos_data_path = "{data_dir}".format(data_dir=sys.argv[2])

for directory in os.listdir(fuzzdb_path):
    os.system(
        'find {0} | grep .txt$ | egrep -v "readme|exploit" | xargs cat |'
        'egrep -v "^#|^$" > {1}'.format(
            os.path.join(fuzzdb_path, directory),
            os.path.join(syntribos_data_path, "{0}.txt".format(directory))))
