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
import os
import shutil


class ExistingPathType(object):
    def _raise_invalid_file(self, filename, exc=None):
        msg = (
            "\nCan't open '{filename}'; not a readable file or dir."
            "\nPlease enter a valid file or dir location.{exception}").format(
                filename=filename,
                exception="\nException: {exc}\n".format(exc=exc))
        raise IOError(msg)

    def __call__(self, string):
        if not os.path.isdir(string) and not os.path.isfile(string):
            self._raise_invalid_file(string)
        return string


class ExistingDirType(ExistingPathType):
    def __call__(self, string):
        if not os.path.isdir(string):
            self._raise_invalid_file(string)
        return string


class ExistingFileType(ExistingPathType):
    def __call__(self, string):
        if not os.path.isfile(string):
            self._raise_invalid_file(string)
        return string


class ContentType(ExistingPathType):
    """Reads a file/directory to collect the contents."""

    def __init__(self, mode):
        self._mode = mode
        self._root = ""

    def _fetch_from_dir(self, string):
        for path, _, files in os.walk(string):
            for file_ in files:
                try:
                    file_path = os.path.join(path, file_)
                    if path is not self._root:
                        subdir = os.path.relpath(path, self._root)
                        yield self._fetch_from_file(file_path, subdir)

                    else:
                        yield self._fetch_from_file(file_path)
                except Exception:
                    print("Skipped %s" % string)

    def _fetch_from_file(self, string, subdir=None):
        # Get the filename here
        relative_path = os.path.split(string)[1]
        if subdir:
            # Path relative to the "templates" directory specified by user
            relative_path = os.path.join(subdir, relative_path)
        try:
            with open(string, self._mode) as fp:
                return relative_path, fp.read()
        except IOError as exc:
            self._raise_invalid_file(string, exc=exc)

    def __call__(self, string):
        """Yield the name and contents of the file(s)

        :param str string: the value supplied as the argument

        :rtype: tuple
        :returns: (file name, file contents)
        """
        if not string:
            return
        super(ContentType, self).__call__(string)

        if os.path.isdir(string):
            self._root = string
            return self._fetch_from_dir(string)
        elif os.path.isfile(string):
            return [self._fetch_from_file(string)]


def delete_file(path):
    os.remove(path)


def delete_dir(dir_path):
    return shutil.rmtree(dir_path)


def file_type(path):
    """Identifies what the type of file is."""
    signature = {
        "\x1f\x8b\x08": "gz",
        "\x42\x5a\x68": "bz2",
        "\x50\x4b\x03\x04": "zip"
    }
    with open(path, "r") as f:
        for sig, f_type in signature.items():
            if f.read(4).startswith(sig):
                return f_type
