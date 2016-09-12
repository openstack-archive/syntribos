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
import random
import uuid


def get_uuid():
    """Generates strings to use where random or unique data is required.

    :returns: universally unique identifiers
    """
    while True:
        random_data = str(uuid.uuid4())
        yield random_data


def fake_port():
    return random.int(0, 65535)


def fake_ip():
    return "{}:{}:{}:{}".format(random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255))


def fake_mac():
    return "{:x}:{:x}:{:x}:{:x}:{:x}:{:x}".format(random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255),
                                                  random.randint(0, 255))


def random_port():
    while True:
        yield fake_port()


def random_ip():
    while True:
        yield fake_ip()


def random_mac():
    while True:
        yield fake_mac()
