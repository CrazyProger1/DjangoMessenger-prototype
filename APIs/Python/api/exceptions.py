class SessionLoadError(Exception):
    pass


class InvalidHostError(Exception):
    pass


class BaseAPIError(Exception):
    def __init__(self, error_key, error_text):
        super(BaseAPIError, self).__init__(error_key + ': ' + error_text)


class WrongDataProvidedError(BaseAPIError):
    pass


class WrongCredentialsProvidedError(BaseAPIError):
    pass


class RefreshExpiredError(BaseAPIError):
    pass
