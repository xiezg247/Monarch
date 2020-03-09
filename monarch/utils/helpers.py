import requests
import requests.adapters


class Retry(object):
    def __init__(self, max_retries=3):
        self._s = requests.Session()
        _http = requests.adapters.HTTPAdapter(max_retries=max_retries)
        _https = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self._s.mount("http://", _http)
        self._s.mount("https://", _https)

    def __getattr__(self, name):
        return getattr(self._s, name)
