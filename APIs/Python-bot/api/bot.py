from .apihelper import APIHelper


class Bot:
    def __init__(self, token: str, host: str = None):
        self.token = token
        self.host = host

        self.name: str | None = None
        self.id: int | None = None
        self.creator_id: int | None = None

        self._api_helper: APIHelper = APIHelper(self.host)

    # def authorize(self):
    #     self._api_helper.get()
