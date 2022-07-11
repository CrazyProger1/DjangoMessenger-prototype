from .services import *


def extract_bot_from_request(request) -> Bot:
    if request.headers.get('BotAuthorization', False):
        return get_bot_by_token(request.headers.get('BotAuthorization'))


def extract_bot_from_scope(scope) -> Bot:
    headers = dict(scope['headers'])

    if headers.get(b'botauthorization', False):
        return get_bot_by_token(headers.get(b'botauthorization').decode())
