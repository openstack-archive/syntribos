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
import syntribos.signal


def server_software(test):
    """Fingerprints the server and possible version.

    Reads response headers and if server software information is present,
    returns a signal with server software  slug.

    :returns: SynSignal
    """
    check_name = "FINGERPRINT"
    strength = 1.0

    if not test.init_signals.ran_check(check_name):
        resp = test.init_resp
    else:
        resp = test.test_resp

    servers = {
        'Apache': 'APACHE',
        'nginx': 'NGINX',
        'Microsoft-IIS': 'IIS',
        'Oracle': 'ORACLE',
        'IBM_HTTP_Server': 'IBM',
        'AmazonS3': 'AMAZON',
        'GSE': 'GSE',
        'lightpd': 'LIGHTPD',
        'WSGIServer': 'WSGI',
        'Express': 'EXPRESS',
        'Servlet': 'TOMCAT',
        'Unknown': 'UNKNOWN'
    }

    if 'Server' in resp.headers:
        server = resp.headers['Server']
    elif 'Powered-by' in resp.headers:
        server = resp.headers['Powered-by']
    elif 'x-server-name' in resp.headers:
        server = resp.headers['x-server-name']
    else:
        server = 'Unknown'

    server_name = servers.get(server, 'UNKNOWN')

    if '/' in server:
        version = server.split('/')[1]
    else:
        version = 0

    text = (
        "Server Details:\n"
        "\tServer Software: {0}\n"
        "\tServer Version: {1}\n").format(server_name, version)

    slug = "SERVER_SOFTWARE_{0}".format(server_name)

    return syntribos.signal.SynSignal(text=text, slug=slug,
                                      strength=strength, check_name=check_name)


def remote_os(test):
    """Returns remote OS info.

    Tries to identity which OS is running on the remote server

    :returns: SynSignal
    """
    check_name = "REMOTE_OS"
    strength = 1.0
    remote_os = test.init_resp.headers.get('X-Distribution', 'UNKNOWN')
    remote_os = remote_os.replace(' ', '_').upper()

    text = (
        'Remote OS Details:\n'
        '\tServer OS: {0}\n').format(remote_os)
    slug = 'SERVER_OS_{0}'.format(remote_os)

    return syntribos.signal.SynSignal(text=text, slug=slug,
                                      strength=strength, check_name=check_name)
