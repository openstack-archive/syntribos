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
# pylint: skip-file
import logging
import sys

from oslo_config import cfg

import syntribos
from syntribos._i18n import _, _LE, _LW   # noqa
from syntribos.utils.file_utils import ContentType
from syntribos.utils.file_utils import ExistingDirType

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
OPTS_REGISTERED = False


def handle_config_exception(exc):
    msg = ""

    if not any(LOG.handlers):
        logging.basicConfig(level=logging.DEBUG)

    if isinstance(exc, cfg.RequiredOptError):
        msg = "Missing option '{opt}'".format(opt=exc.opt_name)
        if exc.group:
            msg += " in group '{}'".format(exc.group)
        CONF.print_help()

    elif isinstance(exc, cfg.ConfigFilesNotFoundError):
        if CONF._args[0] == "init":
            return

        msg = (_("Configuration file specified ('%s') wasn't "
                 "found or was unreadable.") % ",".join(
            CONF.config_file))

    if msg:
        LOG.warning(msg)
        print(syntribos.SEP)
        sys.exit(0)
    else:
        LOG.exception(exc)


syntribos_group = cfg.OptGroup(name="syntribos", title="Main syntribos Config")
user_group = cfg.OptGroup(name="user", title="Identity Config")
test_group = cfg.OptGroup(name="test", title="Test Config")
logger_group = cfg.OptGroup(name="logging", title="Logger config")
remote_group = cfg.OptGroup(name="remote", title="Remote config")


def sub_commands(sub_parser):
    init_parser = sub_parser.add_parser(
        "init",
        help=_("Initialize syntribos environment after "
               "installation. Should be run before any other "
               "commands."))
    init_parser.add_argument(
        "--force", dest="force", action="store_true",
        help=_(
            "Skip prompts for configurable options, force initialization "
            "even if syntribos believes it has already been initialized. If "
            "--custom_install_root isn't specified, we will use the default "
            "options. WARNING: This is potentially destructive! Use with "
            "caution."))
    init_parser.add_argument(
        "--custom_install_root", dest="custom_install_root",
        help=_("Skip prompts for configurable options, and initialize "
               "syntribos in the specified directory. Can be combined "
               "with --force to overwrite existing files."))
    init_parser.add_argument(
        "--no_downloads", dest="no_downloads", action="store_true",
        help=_("Disable the downloading of payload files as part of the "
               "initialization process"))

    download_parser = sub_parser.add_parser(
        "download",
        help=_(
            "Download payload and template files. This command is "
            "configurable according to the remote section of your "
            "config file"))
    download_parser.add_argument(
        "--templates", dest="templates", action="store_true",
        help=_("Download templates"))
    download_parser.add_argument(
        "--payloads", dest="payloads", action="store_true",
        help=_("Download payloads"))

    sub_parser.add_parser("list_tests",
                          help=_("List all available tests"))
    sub_parser.add_parser("run",
                          help=_("Run syntribos with given config"
                                 "options"))
    sub_parser.add_parser("dry_run",
                          help=_("Dry run syntribos with given config"
                                 "options"))


def list_opts():
    results = []
    results.append((None, list_cli_opts()))
    results.append((syntribos_group, list_syntribos_opts()))
    results.append((user_group, list_user_opts()))
    results.append((test_group, list_test_opts()))
    results.append((logger_group, list_logger_opts()))
    results.append((remote_group, list_remote_opts()))
    return results


def register_opts():
    global OPTS_REGISTERED
    if not OPTS_REGISTERED:
        # CLI options
        CONF.register_cli_opts(list_cli_opts())
        # Syntribos options
        CONF.register_group(syntribos_group)
        CONF.register_cli_opts(list_syntribos_opts(), group=syntribos_group)
        # Keystone options
        CONF.register_group(user_group)
        CONF.register_opts(list_user_opts(), group=user_group)
        # Test options
        CONF.register_group(test_group)
        CONF.register_opts(list_test_opts(), group=test_group)
        # Logger options
        CONF.register_group(logger_group)
        CONF.register_opts(list_logger_opts(), group=logger_group)
        # Remote options
        CONF.register_group(remote_group)
        CONF.register_opts(list_remote_opts(), group=remote_group)
        OPTS_REGISTERED = True


def list_cli_opts():
    return [
        cfg.SubCommandOpt(name="sub_command",
                          handler=sub_commands,
                          help=_("Available commands"),
                          title="syntribos Commands"),
        cfg.MultiStrOpt("test-types", dest="test_types", short="t",
                        default=[""], sample_default=["SQL", "XSS"],
                        help=_(
                            "Test types to run against the target API")),
        cfg.MultiStrOpt("excluded-types", dest="excluded_types", short="e",
                        default=[""], sample_default=["SQL", "XSS"],
                        help=_("Test types to be excluded from "
                               "current run against the target API")),
        cfg.BoolOpt("colorize", dest="colorize", short="cl", default=False,
                    help=_("Enable color in syntribos terminal output")),
        cfg.StrOpt("outfile", short="o",
                   sample_default="out.json", help=_("File to print "
                                                     "output to")),
        cfg.StrOpt("format", dest="output_format", short="f", default="json",
                   choices=["json"], ignore_case=True,
                   help=_("The format for outputting results")),
        cfg.StrOpt("min-severity", dest="min_severity", short="S",
                   default="LOW", choices=syntribos.RANKING,
                   help=_("Select a minimum severity for reported "
                          "defects")),
        cfg.StrOpt("min-confidence", dest="min_confidence", short="C",
                   default="LOW", choices=syntribos.RANKING,
                   help=_("Select a minimum confidence for reported "
                          "defects"))
    ]


def list_syntribos_opts():
    def wrap_try_except(func):
        def wrap(*args):
            try:
                func(*args)
            except IOError:
                msg = _(
                    "\nCan't open a file or directory specified in the "
                    "config file under the section `[syntribos]`; verify "
                    "if the path exists.\nFor more information please refer "
                    "the debug logs.")
                print(msg)
                exit(1)
        return wrap
    return [
        cfg.StrOpt("endpoint", default="",
                   sample_default="http://localhost/app",
                   help=_("The target host to be tested")),
        cfg.Opt("templates", type=ContentType("r", 0),
                default="",
                sample_default="~/.syntribos/templates",
                help=_("A directory of template files, or a single "
                       "template file, to test on the target API")),
        cfg.StrOpt("payloads", default="",
                   sample_default="~/.syntribos/data",
                   help=_(
                       "The location where we can find syntribos'"
                       "payloads")),
        cfg.MultiStrOpt("exclude_results",
                        default=[""],
                        sample_default=["500_errors", "length_diff"],
                        help=_(
                            "Defect types to exclude from the "
                            "results output")),
        cfg.Opt("custom_root", type=wrap_try_except(ExistingDirType()),
                short="c",
                sample_default="/your/custom/root",
                help=_(
                    "The root directory where the subfolders that make up"
                    " syntribos' environment (logs, templates, payloads, "
                    "configuration files, etc.)")),
    ]


def list_user_opts():
    return [
        cfg.StrOpt("version", default="v2.0",
                   help=_("keystone version"), choices=["v2.0", "v3"]),
        cfg.StrOpt("username", default="",
                   help=_("keystone username")),
        cfg.StrOpt("password", default="",
                   help=_("keystone user password"),
                   secret=True),
        cfg.StrOpt("user_id", default="",
                   help=_("Keystone user ID"), secret=True),
        cfg.StrOpt("token", default="", help=_("keystone auth token"),
                   secret=True),
        cfg.StrOpt("endpoint", default="",
                   help=_("keystone endpoint URI")),
        cfg.StrOpt("domain_name", default="",
                   help=_("keystone domain name")),
        cfg.StrOpt("project_id", default="",
                   help=_("keystone project id")),
        cfg.StrOpt("project_name", default="",
                   help=_("keystone project name")),
        cfg.StrOpt("domain_id", default="",
                   help=_("keystone domain id")),
        cfg.StrOpt("tenant_name", default="",
                   help=_("keystone tenant name")),
        cfg.StrOpt("tenant_id", default="",
                   help=_("keystone tenant id")),
        cfg.StrOpt("serialize_format", default="json",
                   help=_("Type of request body")),
        cfg.StrOpt("deserialize_format", default="json",
                   help=_("Type of response body")),
        cfg.IntOpt("token_ttl", default=1800,
                   help=_("Time to live for token in seconds"))

    ]


def list_test_opts():
    return [
        cfg.FloatOpt("length_diff_percent", default=1000.0,
                     help=_(
                         "Percentage difference between initial request "
                         "and test request body length to trigger a signal")),
        cfg.FloatOpt("time_diff_percent", default=1000.0,
                     help=_(
                         "Percentage difference between initial response "
                         "time and test response time to trigger a signal")),
        cfg.IntOpt("max_time", default=10,
                   help=_(
                       "Maximum absolute time (in seconds) to wait for a "
                       "response before triggering a timeout signal")),
        cfg.IntOpt("max_length", default=500,
                   help=_(
                       "Maximum length (in characters) of the response text")),
        cfg.ListOpt("failure_keys", default="[`syntax error`]",
                    help=_(
                        "Comma seperated list of keys for which the test "
                        "would fail."))
    ]


def list_logger_opts():
    # TODO(unrahul): Add log formating and verbosity options
    return [
        cfg.BoolOpt("http_request_compression", default=True,
                    help=_(
                        "Request content compression to compress fuzz "
                        "strings present in the http request content.")),
        cfg.StrOpt("log_dir", default="",
                   sample_default="~/.syntribos/logs",
                   help=_(
                       "Where to save debug log files for a syntribos run"
                   ))
    ]


def list_remote_opts():
    """Method defining remote URIs for payloads and templates."""
    return [
        cfg.StrOpt(
            "cache_dir",
            default="",
            help=_("Base directory where cached files can be saved")),
        cfg.StrOpt(
            "payloads_uri",
            default=("https://github.com/openstack/syntribos-payloads/"
                     "archive/master.tar.gz"),
            help=_("Remote URI to download payloads.")),
        cfg.StrOpt(
            "templates_uri",
            default=("https://github.com/openstack/"
                     "syntribos-openstack-templates/archive/master.tar.gz"),
            help=_("Remote URI to download templates.")),
        cfg.BoolOpt("enable_cache", default=True,
                    help=_(
                        "Cache remote template & payload resources locally")),
    ]
