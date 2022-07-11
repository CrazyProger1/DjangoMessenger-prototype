from .services import *


def extract_bot(request) -> Bot:
    if request.headers.get('BotAuthorization', False):
        return get_bot_by_token(request.headers.get('BotAuthorization'))
