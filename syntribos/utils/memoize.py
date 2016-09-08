# Copyright 2016 Rackspace
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
from functools import wraps
from time import time

from oslo_config import cfg

CONF = cfg.CONF


def memoize(func):
    """Caches the result of a function call

    This is not intended to memoize functions with mutable arguments
    """
    memoized_calls = {}

    @wraps(func)
    def decorate(*args, **kwargs):
        ttl = time() + CONF.user.token_ttl
        func_id = args, frozenset(kwargs.items())
        if memoized_calls.get(func_id):
            time_left = memoized_calls[func_id]["ttl"] - time()
            if time_left > 0:
                return memoized_calls[func_id]["ret_val"]
        memoized_calls[func_id] = {"ret_val": func(*args, **kwargs),
                                   "ttl": ttl}
        return memoized_calls[func_id]["ret_val"]
    return decorate
