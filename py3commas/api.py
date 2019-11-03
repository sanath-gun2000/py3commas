import hashlib
import hmac
import requests
from .config import API_URL, API_VERSION, APIS


class Api:

    def __init__(self, key: str, secret: str):
        self.url = API_URL
        self.version = API_VERSION
        self.key = key
        self.secret = secret

    def _generate_signature(self, path: str, data: str) -> str:
        byte_key = str.encode(self.secret)
        message = str.encode(self.version + path + data)
        signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return signature

    def _make_request(self, method: str, path: str, params: any):
        signature = self._generate_signature(path, params)

        response = requests.request(
            method=method,
            url=self.url + self.version + path + '?' + params,
            headers={
                'APIKEY': self.key,
                'Signature': signature
            }
        )
        return response

    def request(self, api_domain: str, api_name: str = '', _id: str = None):
        api = APIS[api_domain][api_name]
        api_path = api[1]
        if '{id}' in api_path:
            api_path = api_path.replace('{id}', _id)
        self._make_request(api[0], api_domain + api_path, '')
