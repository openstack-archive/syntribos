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


def memoize(func):
    """Caches the result of a function call

    This is not intended to memoize functions with mutable arguments
    """
    memoized_calls = {}

    @wraps(func)
    def decorate(*args, **kwargs):
        if args in memoized_calls:
            return memoized_calls[args]
        else:
            memoized_calls[args] = func(*args, **kwargs)
            return memoized_calls[args]
    return decorate
