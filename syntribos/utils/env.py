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
import shutil
import sys

from oslo_config import cfg
from six.moves import input

import syntribos

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
        user = os.getlogin() or os.environ.get("USER")
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
    custom_root = CONF.syntribos.custom_root

    if custom_root:
        return expand_path(custom_root)

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


def get_log_dir_name():
    """Returns the directory where log files would be saved."""
    log_dir = CONF.logging.log_dir
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%X.%f")
    log_path = "{time}".format(time=time_str.split(".")[0])
    log_path = os.path.join(log_dir, log_path)
    return log_path


def safe_makedirs(path, force=False):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except (OSError, IOError):
            LOG.exception("Error creating folder (%s).", path)
    elif os.path.exists(path) and force:
        try:
            shutil.rmtree(path)
            os.makedirs(path)
        except (OSError, IOError):
            LOG.exception("Error overwriting existing folder (%s).", path)
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

    return (root_dir, payloads, templates, log_dir)


def create_conf_file(created_folders=None):
    global FILE
    root, payloads, templates, logs = created_folders
    conf_file = os.path.join(root, FILE)
    # Create default configuration file
    with open(conf_file, "w") as f:
        custom_root = CONF.sub_command.custom_install_root or ""
        if custom_root:
            custom_root = "custom_root={0}".format(custom_root)
        template = (
            "# syntribos barebones configuration file\n"
            "# You should update this with your desired options!\n"
            "[syntribos]\n"
            "endpoint=http://127.0.0.1:80\n"
            "payloads={payloads}\n"
            "templates={templates}\n"
            "{custom_root}\n"
            "[logging]\n"
            "log_dir={logs}\n"
        ).format(
            payloads=payloads, templates=templates, custom_root=custom_root,
            logs=logs)
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
    custom_root = CONF.sub_command.custom_install_root or ""
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
            prompt = ("Syntribos has not been initialized. By default, this "
                      "process will create a '.syntribos' folder with a "
                      "barebones configuration file, and sub-folders for "
                      "templates, debug logs, and payloads.").format(
                          get_syntribos_root())
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
    conf_file = create_conf_file(folders_created)

    # Grab payloads
    # Grab templates

    print("Syntribos has been initialized!")
    print("Folders created:\n\t{0}".format("\n\t".join(folders_created)))
    print("Configuration file:\n\t{0}".format(conf_file))
    print("\nYou'll need to edit your configuration file to specify the "
          "endpoint to test and any other configuration options you want.")
    print(syntribos.SEP)


def is_syntribos_initialized():
    """Determine whether syntribos has been set up properly.

    For testing whether or not the user has e.g. run ```syntribos init``` or
    otherwise created the necessary folders/files to run syntribos
    """
    if not os.path.exists(get_syntribos_root()):
        return False

    if os.path.exists(get_default_conf_file()):
        return True

    return False
