# Copyright 2015-2016 Rackspace
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
import logging
import os
import sys

from oslo_config import cfg

import syntribos

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def handle_config_exception(exc):
    msg = ""

    if isinstance(exc, cfg.RequiredOptError):
        msg = "Missing option '{opt}'".format(opt=exc.opt_name)
        if exc.group:
            msg += " in group '{}'".format(exc.group)
        CONF.print_help()

    elif isinstance(exc, cfg.ConfigFilesNotFoundError):
        msg = ("Configuration file specified ('{config}') wasn't "
               "found or was unreadable.").format(
            config=",".join(CONF.config_file))

    if msg:
        LOG.warning(msg)
        print("=" * 80)
        sys.exit(0)
    else:
        raise exc


class ExistingPathType(object):

    def _raise_invalid_file(self, filename, exc=None):
        msg = ("\nCan't open '{filename}'; not a readable file or dir."
               "\nPlease enter a valid file or dir location.{exception}"
               ).format(filename=filename,
                        exception="\nEXCEPTION: {exc}\n".format(exc=exc))
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


class TemplateType(ExistingPathType):

    """Reads a file/directory to collect request templates."""

    def __init__(self, mode, bufsize):
        self._mode = mode
        self._bufsize = bufsize

    def _fetch_from_dir(self, string):
        for path, _, files in os.walk(string):
            for file_ in files:
                file_path = os.path.join(path, file_)
                yield self._fetch_from_file(file_path)

    def _fetch_from_file(self, string):
        try:
            with open(string, self._mode, self._bufsize) as fp:
                return os.path.split(fp.name)[1], fp.read()
        except IOError as exc:
            self._raise_invalid_file(string, exc=exc)

    def __call__(self, string):
        """Yield the name and contents of the file(s)

        :param str string: the value supplied as the argument

        :rtype: tuple
        :returns: (file name, file contents)
        """
        super(TemplateType, self).__call__(string)

        if os.path.isdir(string):
            return self._fetch_from_dir(string)
        elif os.path.isfile(string):
            return [self._fetch_from_file(string)]


syntribos_group = cfg.OptGroup(name="syntribos", title="Main Syntribos Config")
user_group = cfg.OptGroup(name="user", title="Identity Config")
test_group = cfg.OptGroup(name="test", title="Test Config")


def list_opts():
    results = []
    results.append((None, list_cli_opts()))
    results.append((None, list_syntribos_opts()))
    results.append((user_group, list_user_opts()))
    results.append((test_group, list_test_opts()))
    return results


def register_opts():
    # CLI options
    CONF.register_cli_opts(list_cli_opts())
    # Syntribos options
    CONF.register_group(syntribos_group)
    CONF.register_opts(list_syntribos_opts(), group=syntribos_group)
    # Keystone options
    CONF.register_group(user_group)
    CONF.register_opts(list_user_opts(), group=user_group)
    # Test options
    CONF.register_group(test_group)
    CONF.register_opts(list_test_opts(), group=test_group)


def list_cli_opts():
    return [
        cfg.MultiStrOpt("test-types", dest="test_types", short="t",
                        default=[""],
                        help="Test types to run against the target API"),
        cfg.BoolOpt("verbose", short="v", default=False,
                    help="Print more information to output"),
        cfg.BoolOpt("dry-run", dest="dry_run", short="D", default=False,
                    help="Don't run tests, just print them out to console"),
        cfg.StrOpt("outfile", short="o", default=None,
                   help="File to print output to"),
        cfg.StrOpt("format", dest="output_format", short="f", default="json",
                   choices=["json"], ignore_case=True,
                   help="The format for outputting results"),
        cfg.StrOpt("min-severity", dest="min_severity", short="S",
                   default="LOW", choices=syntribos.RANKING,
                   help="Select a minimum severity for reported defects"),
        cfg.StrOpt("min-confidence", dest="min_confidence", short="C",
                   default="LOW", choices=syntribos.RANKING,
                   help="Select a minimum confidence for reported defects")
    ]


def list_syntribos_opts():
    return [
        cfg.StrOpt("endpoint", default="",
                   sample_default="http://localhost/app", required=True,
                   help="The target host to be tested"),
        cfg.Opt("templates", type=TemplateType('r', 0), required=True,
                help="A directory of template files, or a single template "
                     "file, to test on the target API"),
        cfg.StrOpt("payload_dir", default="", required=True,
                   help="The location where we can find Syntribos' payloads"),
        cfg.StrOpt("log_dir", default="", required=True,
                   help="Where to save debug log files for a Syntribos run")
    ]


def list_user_opts():
    return [
        cfg.StrOpt("username", default="", help="Keystone username"),
        cfg.StrOpt("password", default="", help="Keystone user password",
                   secret=True),
        cfg.StrOpt("user_id", default="",
                   help="Keystone user ID", secret=True),
        cfg.StrOpt("project", default="", help="Keystone project ID"),
        cfg.StrOpt("token", default="", help="Keystone auth token",
                   secret=True),
        cfg.StrOpt("endpoint", default="", help="Keystone endpoint URI"),
        cfg.StrOpt("domain_name", default="", help="Keystone domain name"),
        cfg.StrOpt("domain_id", default="", help="Keystone domain id"),
        cfg.StrOpt("tenant_name", default="", help="Keystone tenant name"),
        cfg.StrOpt("tenant_id", default="", help="Keystone tenant id"),
        cfg.StrOpt("serialize_format", default="json",
                   help="Type of request body"),
        cfg.StrOpt("deserialize_format", default="json",
                   help="Type of response body"),

    ]


def list_test_opts():
    # TODO(cneill): Discover other config options from tests dynamically
    return [
        cfg.FloatOpt("length_diff_percent", default=200.0,
                     help="Percentage difference between initial request "
                          "and test request body length to trigger a signal"),
        cfg.FloatOpt("time_diff_percent", default=200.0,
                     help="Perecentage difference between initial response "
                          "time and test response time to trigger a signal"),
        cfg.IntOpt("max_time", default=10,
                   help="Maximum absolute time (in seconds) to wait for a "
                        "response before triggering a timeout signal")
    ]
