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
import datetime
import logging
import os
import pwd
import shutil
import sys

from oslo_config import cfg
import requests
from six.moves import input

import syntribos
from syntribos._i18n import _
from syntribos.utils import remotes

FOLDER = ".syntribos"
FILE = "syntribos.conf"
CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def expand_path(path):
    if not path:
        return ""
    elif "~" in path:
        path = os.path.expanduser(path)
    return os.path.abspath(path)


def get_user_home_root():
    global FOLDER
    user = os.environ.get("SUDO_USER")
    if not user:
        try:
            user = os.environ.get("USER") or os.getlogin()
        except OSError as e:
            # Refer https://mail.python.org/pipermail/python-bugs-list/
            # 2002-July/012691.html
            LOG.error("Exception thrown in : %s", e)
            user = pwd.getpwuid(os.getuid())[0]
    home_path = "~{0}/{1}".format(user, FOLDER)
    return expand_path(home_path)


def is_venv():
    # Virtualenv sets "sys.real_prefix" and replaces "sys.prefix"
    return hasattr(sys, "real_prefix")


def get_venv_root():
    # Virtualenv detection
    path = ""
    if is_venv():
        path = os.path.abspath(os.path.join(sys.prefix, FOLDER))
    return path


def get_syntribos_root():
    """This determines the proper path to use as syntribos' root directory."""
    path = ""
    try:
        custom_root = (
            CONF.syntribos.custom_root or CONF.custom_root or ""
        )
        if custom_root:
            return expand_path(custom_root)
    except Exception:
        raise
    home_root = get_user_home_root()

    # Virtualenv detection
    if get_venv_root():
        path = get_venv_root()

    # Use home dir if syntribos folder already exists, or no virtualenv found
    if os.path.exists(home_root) or not path:
        path = home_root

    return path


def get_syntribos_path(*args):
    return os.path.abspath(os.path.join(get_syntribos_root(), *args))


def get_default_conf_file():
    global FILE
    return get_syntribos_path(FILE)


def get_log_dir_name(log_path=""):
    """Returns the directory where log files would be saved."""
    log_dir = CONF.logging.log_dir or log_path
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%X.%f")
    log_path = "{time}".format(time=time_str.split(".")[0])
    log_path = os.path.join(log_dir, log_path)
    return log_path


def safe_makedirs(path, force=False):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except (OSError, IOError):
            LOG.exception(_("Error creating folder (%s).") % path)
    elif os.path.exists(path) and force:
        try:
            shutil.rmtree(path)
            os.makedirs(path)
        except (OSError, IOError):
            LOG.exception(
                _("Error overwriting existing folder (%s).") % path)
    else:
        LOG.warning("Folder was already found (%s). Skipping.", path)


def create_env_dirs(root_dir, force=False):
    # Create syntribos environment folder
    safe_makedirs(root_dir, force)

    # Create payloads folder
    payloads = os.path.join(root_dir, "payloads")
    safe_makedirs(payloads, force)

    # Create templates folder
    templates = os.path.join(root_dir, "templates")
    safe_makedirs(templates, force)

    # Create logs folder
    log_dir = os.path.join(root_dir, "logs")
    safe_makedirs(log_dir, force)

    return tuple(os.path.abspath(x)
                 for x in (root_dir, payloads, templates, log_dir))


def create_conf_file(created_folders=None, remote_path=None):
    global FILE
    root, payloads, templates, logs = created_folders
    conf_file = os.path.join(root, FILE)
    # Create default configuration file
    with open(conf_file, "w") as f:
        custom_root = (
            CONF.syntribos.custom_root or CONF.custom_root or ""
        )
        if custom_root:
            custom_root = (
                "# Any changes in the [DEFAULT] section will overwrite all "
                "command line options\n"
                "# [DEFAULT]\n"
                "# custom_root={0}"
                "# force=true\n\n"
            ).format(custom_root)
        template = (
            "# syntribos barebones configuration file\n"
            "# You should update this with your desired options!\n\n"
            "{custom_root}"
            "[syntribos]\n"
            "endpoint=http://127.0.0.1:8080\n"
            "payloads={payloads}\n"
            "templates={templates}\n\n"
            "[logging]\n"
            "log_dir={logs}\n"
        ).format(
            payloads=remote_path if remote_path else payloads,
            templates=templates, custom_root=custom_root, logs=logs)
        f.write(template)
    return conf_file


def initialize_syntribos_env():
    """Sets up payloads, config, etc. for syntribos after installation."""

    def prompt_yes(prompt):
        answer = input(prompt).lower()
        return answer == "yes" or answer == "y"

    def prompt_yes_or_quit(prompt):
        prompt = ("{0}\n\tType 'yes' or 'y' to continue, anything else "
                  "to quit: ").format(prompt)
        if not prompt_yes(prompt):
            print("Aborting syntribos initialization.")
            exit(0)
        return True

    def prompt_yes_or_continue(prompt):
        prompt = ("{0}\n\tType 'yes' or 'y' to continue, anything else "
                  "for more options: ").format(prompt)
        return prompt_yes(prompt)

    global FILE
    logging.basicConfig(level=logging.DEBUG)
    root_dir = get_venv_root() if is_venv() else get_user_home_root()

    force = CONF.sub_command.force
    custom_root = CONF.syntribos.custom_root or CONF.custom_root or ""
    if custom_root:
        root_dir = custom_root
    elif CONF.sub_command.force:
        pass
    else:
        # Check if we've already initalized env so we don't overwrite anything
        if is_syntribos_initialized():
            prompt = ("It seems syntribos has already been initialized.")
            prompt_yes_or_quit(prompt)

        else:
            if not CONF.sub_command.no_downloads:
                prompt = ("Syntribos has not been initialized. By default, "
                          "this process will create a '.syntribos' folder\n "
                          "with a barebones configuration file, and "
                          "sub-folders for templates, debug logs, and\n "
                          "payloads. Syntribos will also attempt to download "
                          "payload files, which are necessary for fuzz\n "
                          "tests to run. To avoid this behavior, run this "
                          "command again with the --no_downloads flag")
            else:
                prompt = ("Syntribos has not been initialized. By default, "
                          "this process will create a '.syntribos' folder\n "
                          "with a barebones configuration file, and "
                          "sub-folders for templates, debug logs, and\n "
                          "payloads. Syntribos will not attempt to download "
                          "any files during the initialization process.")
            prompt_yes_or_quit(prompt)

        if is_venv():
            prompt = "Virtual environment detected. Install to {0}?".format(
                get_venv_root())
            if prompt_yes_or_continue(prompt):
                root_dir = get_venv_root()
            else:
                prompt = ("Install to your home directory ({0})?").format(
                    get_user_home_root())
                if prompt_yes_or_quit(prompt):
                    root_dir = get_user_home_root()

    folders_created = create_env_dirs(root_dir, force=force)

    # Grab payloads
    logging.disable(logging.ERROR)  # Don't want to log to console here...

    payloads_dir = folders_created[1]
    if not CONF.sub_command.no_downloads:
        print(
            _("\nDownloading payload files to %s...") % payloads_dir)
        try:
            remote_path = remotes.get(CONF.remote.payloads_uri, payloads_dir)
            conf_file = create_conf_file(folders_created, remote_path)
            print(_("Download successful!"))
        except (requests.ConnectionError, IOError):
            print(_("Download failed. If you would still like to download"
                    " payload files, please consult our documentation"
                    " about the 'syntribos download' command or do so"
                    " manually."))
            conf_file = create_conf_file(folders_created)
    else:
        conf_file = create_conf_file(folders_created)

    logging.disable(logging.NOTSET)

    print(_("\nSyntribos has been initialized!"))
    print(
        _("Folders created:\n\t%s") % "\n\t".join(folders_created))
    print(_("Configuration file:\n\t%s") % conf_file)
    print(_(
        "\nYou'll need to edit your configuration file to specify the "
        "endpoint to test and any other configuration options you want."))
    print(_(
        "\nBy default, syntribos does not ship with any template files, "
        "which are required for syntribos to run. However, we provide a\n "
        "'syntribos download' command to fetch template files remotely. "
        "Please see our documentation for this subcommand, or run\n "
        "'syntribos download --templates' to download our default set of "
        "OpenStack templates."))
    print(syntribos.SEP)


def is_syntribos_initialized():
    """Determine whether syntribos has been set up properly.

    For testing whether or not the user has e.g. run ```syntribos init``` or
    otherwise created the necessary folders/files to run syntribos
    """
    if not os.path.exists(get_syntribos_root()):
        return False
    flat_list = []
    for ele in [get_default_conf_file(), CONF.config_file, CONF.config_dir]:
        if ele and isinstance(ele, str):
            flat_list.append(ele)
        elif ele and isinstance(ele, list):
            for s in ele:
                flat_list.append(s)

    if any([os.path.exists(conf_file) for conf_file in flat_list]):
        return True

    return False


def download_wrapper():
    """Provides wrapper method to use in 'syntribos download' subcommand."""
    templates_uri = CONF.remote.templates_uri
    payloads_uri = CONF.remote.payloads_uri

    templates_dir = (CONF.remote.cache_dir or
                     os.path.join(get_syntribos_root(), "templates"))
    payloads_dir = (CONF.remote.cache_dir or
                    os.path.join(get_syntribos_root(), "payloads"))

    if not CONF.sub_command.templates and not CONF.sub_command.payloads:
        print(
            _(
                "Please specify the --templates flag and/or the --payloads"
                "flag to this command.\nNo files have been downloaded.\n"))

    if CONF.sub_command.templates:
        print(_(
            "Downloading template files from %(uri)s to %(dir)s..."
        ) % {"uri": templates_uri, "dir": templates_dir})
        try:
            remotes.get(templates_uri, templates_dir)
            print(_(
                "Download successful! To use these templates, edit your "
                "config file to update the location of templates."))
        except Exception:
            print(_(
                "Template download failed. Our documentation contains "
                "instructions to provide templates manually."))
            exit(1)

    if CONF.sub_command.payloads:
        print(_(
            "Downloading payload files from %(uri)s to %(dir)s...\n") % {
                "uri": payloads_uri, "dir": payloads_dir})
        try:
            remotes.get(payloads_uri, payloads_dir)
            print(_(
                "Download successful! To use these payloads, edit your "
                "config file to update the location of payloads."))
        except Exception:
            print(_(
                "Payload download failed. Our documentation contains "
                "instructions to provide payloads manually."))
            exit(1)
