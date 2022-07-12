from rest_framework_simplejwt import authentication
from bots.extractors import extract_bot_from_request
from bots.models import Bot
from rest_framework import request as rq


class BotSupportingJWTAuthentication(authentication.JWTAuthentication):
    def authenticate(self, request: rq.Request):
        request.bot = None

        if request.headers.get('BotAuthorization'):
            return self.authenticate_bot(request)

        return super(BotSupportingJWTAuthentication, self).authenticate(request)

    def authenticate_bot(self, request):
        bot = extract_bot_from_request(request)
        request.bot = bot

        return super(BotSupportingJWTAuthentication, self).authenticate(request)
