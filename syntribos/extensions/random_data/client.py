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
import datetime
import random
import string
import time
import uuid

import six


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


def random_string(n=10, string_type="lower"):
    if string_type == "lower":
        string_type = string.ascii_lowercase
    elif string_type == "upper":
        string_type = string.ascii_uppercase
    else:
        string_type = string.ascii_letters
    while True:
        r = "".join(random.choice(string_type) for _ in range(n))
        yield r


def random_integer(beg=0, end=1478029570):
    # The default value of end is a valid epoch time, this is done so that
    # random intger can then be used to generate random epoch as well.
    while True:
        yield random.randint(beg, end)


def random_utc_datetime():
    """Returns random utc date time."""
    while True:
        offset = six.next(random_integer())
        epoch = time.time() - offset
        ts = datetime.datetime.fromtimestamp(epoch).strftime(
            "%Y-%m-%d %H:%M:%S")
        yield ts
