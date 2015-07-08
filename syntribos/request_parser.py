import urlparse

from cafe.engine.behaviors import BaseBehavior


class RequestObject(object):
    def __init__(
            self, method, url, headers=None, params=None, data=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or ""


class RequestCreator(BaseBehavior):
    @staticmethod
    def _parse(string, endpoint):
        params = None
        lines = string.splitlines()
        method, url, http_version = lines[0].split()
        url = url.split("?", 1)
        if len(url) > 1:
            params = {}
            for param in url[1].split("&"):
                param = param.split("=", 1)
                if len(param) > 1:
                    params[param[0]] = param[1]
                else:
                    params[param[0]] = ""
        url = url[0]
        url = urlparse.urljoin(endpoint, url)
        for index, line in enumerate(lines):
            if line == "":
                break
        headers = {}
        for line in lines[1:index]:
            key, value = line.split(":", 1)
            headers[key] = value.strip()
        data = "\n".join(lines[index+1:])
        return RequestObject(method, url, headers, params, data)

    @classmethod
    def create_request():
        pass