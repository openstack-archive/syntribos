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
from functools import wraps
import logging
import os
import tarfile
import tempfile

from oslo_config import cfg

from syntribos.clients.http.client import SynHTTPClient

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
temp_dirs = []
remote_dirs = []


def cache(func):
    """A method to cache return values of any method."""
    cached_content = {}

    @wraps(func)
    def cached_func(*args, **kwargs):
        if CONF.remote.enable_cache:
            try:
                return cached_content[args]
            except KeyError:
                return cached_content.setdefault(args, func(*args, **kwargs))
        return func(*args, **kwargs)
    return cached_func


def download(uri, cache_dir=None):
    """A simple file downloader.

    A simple file downloader which returns the absolute
    path to where the file has been saved. In case of tar
    files the absolute patch excluding .tar extension is
    passed.

    :param str uri: The remote uri of the file
    :param str  cache_dir: The directory name/handle
    :returns str: Absolute path to the downloaded file
    """
    global temp_dirs
    global remote_dirs
    if not cache_dir:
        cache_dir = tempfile.mkdtemp()
        temp_dirs.append(cache_dir)
    remote_dirs.append(cache_dir)
    log_string = "Remote file location: {}".format(remote_dirs)
    LOG.debug(log_string)
    resp, signals = SynHTTPClient().request("GET", uri)
    os.chdir(cache_dir)
    saved_umask = os.umask(0o77)
    fname = uri.split("/")[-1]
    try:
        with open(fname, 'w') as fh:
            fh.write(resp.content)
        return os.path.abspath(fname)
    except IOError:
        LOG.error("IOError in writing the downloaded file to disk.")
    finally:
        os.umask(saved_umask)


def file_type(path):
    """Identifies what the type of file is."""
    signature = {
        "\x1f\x8b\x08": "gz",
        "\x42\x5a\x68": "bz2",
        "\x50\x4b\x03\x04": "zip"
    }
    with open(path) as f:
        for sig, f_type in signature.items():
            if f.read(4).startswith(sig):
                return f_type


def extract_tar(abs_path):
    """Extract a gzipped tar file from the given absolute_path

    :param str abs_path: The absolute path to the tar file
    :returns str untar_dir: The absolute path to untarred file
    """
    work_dir, tar_file = os.path.split(abs_path)
    os.chdir(work_dir)
    try:
        os.mkdir("remote")
    except OSError:
        LOG.debug("path exists already, not creating remote directory.")
    remote_path = os.path.abspath("remote")

    def safe_paths(tar_meta):
        """Makes sure all tar file paths are relative to the base path

        Orignal from https://stackoverflow.com/questions/
        10060069/safely-extract-zip-or-tar-using-python

        :param tarfile.TarFile tar_meta: TarFile object
        :returns tarfile:TarFile fh: TarFile object
        """
        for fh in tar_meta:
            each_f = os.path.abspath(os.path.join(work_dir, fh.name))
            if os.path.realpath(each_f).startswith(work_dir):
                yield fh

    with tarfile.open(tar_file, mode="r:gz") as tarf:
        tarf.extractall(path=remote_path, members=safe_paths(tarf))
    os.remove(abs_path)
    return remote_path


@cache
def get(uri):
    """Entry method for download method

    :param str uri: A formatted remote URL of a file
    :param str: Absolute path to the downloaded content
    """
    user_base_dir = CONF.remote.cache_dir
    if user_base_dir:
        try:
            temp = tempfile.TemporaryFile(dir=os.path.abspath(user_base_dir))
            temp.close()
        except OSError:
            LOG.error("Failed to write remote files to: {}".format(
                os.path.abspath(user_base_dir)))
            exit(1)
        abs_path = download(uri, os.path.abspath(user_base_dir))
    else:
        abs_path = download(uri)
    if not file_type(abs_path) == "gz":
        msg = "Not a gz file, returning abs_path"
        LOG.debug(msg)
        return abs_path
    return extract_tar(abs_path)
