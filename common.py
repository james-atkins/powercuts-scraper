from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

RETRIES = 5
TIMEOUT = 5

# Force ciphers
# https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop("timeout", TIMEOUT)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return super().send(request, **kwargs)


def make_session():
    session = Session()
    retries = Retry(total=RETRIES, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("http://", TimeoutHTTPAdapter(max_retries=retries))
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    return session
