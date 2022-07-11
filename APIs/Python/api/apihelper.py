import requests
import websocket
import rel

from .config import *
from .exceptions import *

_instances = {}


def singleton(cls):
    def wrapper(*args, **kwargs):
        if cls in _instances.keys():
            return _instances.get(cls)

        _instances.update({cls: cls(*args, **kwargs)})
        return _instances.get(cls)

    return wrapper


@singleton
class APIHelper:
    SUCCESS_CODES = (200, 201)

    def __init__(self, host: str = None):
        self.host = HOST or host
        self._adjust_websocket_host()

    def _adjust_websocket_host(self):
        if 'https' in self.host:
            self.websocket_host = self.host.replace('https', 'ws')
        elif 'http' in self.host:
            self.websocket_host = self.host.replace('http', 'ws')
        else:
            raise InvalidHostError('The host must look like http://... or https://...')

    def set_host(self, host: str):
        self.host = host
        self._adjust_websocket_host()

    def _form_url(self, obj: str):
        return self.host + 'api/' + API_VERSION + '/' + obj + '/'

    @staticmethod
    def _form_headers(access_token: str = None) -> dict | None:
        if not access_token:
            return None

        headers = {
            'Authorization': TOKEN_KEYWORD + ' ' + access_token
        }
        return headers

    def _handle_errors(self, response, **exception_classes) -> requests.Response:
        if response.status_code not in self.SUCCESS_CODES:

            exception = exception_classes.get(f'error{response.status_code}')
            if not exception:
                return response

            errors = response.json()
            error_key = tuple(errors.keys())[0]

            error_text = errors[error_key]
            if isinstance(error_text, list) or isinstance(error_text, tuple):
                error_text = error_text[0]

            raise exception(error_key, error_text)

        return response

    def post(self, json: dict, obj: str = 'users', access_token: str = None, **exception_classes) -> requests.Response:
        response = requests.post(
            url=self._form_url(obj),
            json=json,
            headers=self._form_headers(access_token)
        )

        return self._handle_errors(response, **exception_classes)

    def put(self,
            json: dict,
            obj: str = 'users',
            access_token: str = None,
            partially: bool = False,
            **exception_classes
            ) -> requests.Response:

        if not partially:
            return self._handle_errors(requests.put(
                url=self._form_url(obj),
                json=json,
                headers=self._form_headers(access_token)
            ), **exception_classes)
        return self._handle_errors(requests.patch(
            url=self._form_url(obj),
            json=json,
            headers=self._form_headers(access_token)
        ), **exception_classes)

    def get(self, obj: str = 'users', access_token: str = None, params: dict = None, **exception_classes):
        return self._handle_errors(requests.get(
            url=self._form_url(obj),
            headers=self._form_headers(access_token),
            params=params
        ), **exception_classes)

    def delete(self, obj: str = 'users', access_token: str = None, **exception_classes):
        return self._handle_errors(
            requests.delete(
                url=self._form_url(obj),
                headers=self._form_headers(access_token),

            ),
            **exception_classes
        )

    def connect_to_chat(self, chat_id: int, access_token: str = None):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(f"{self.websocket_host}ws/chat/{chat_id}/",
                                    header=self._form_headers(access_token))

        ws.run_forever(dispatcher=rel)
        return ws
