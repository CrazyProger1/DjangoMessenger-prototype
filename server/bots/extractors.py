from .services import *


def extract_bot_from_request(request) -> Bot:
    if request.headers.get('BotAuthorization', False):
        return get_bot_by_token(request.headers.get('BotAuthorization'))


def extract_bot_from_scope(scope) -> Bot:
    if scope.headers.get('BotAuthorization', False):
        return get_bot_by_token(scope['headers'].get('BotAuthorization'))
