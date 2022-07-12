class InvalidHostError(Exception):
    pass


class BaseAPIError(Exception):
    def __init__(self, error_key, error_text):
        if error_key == 'detail':
            super(BaseAPIError, self).__init__(error_text)
        else:
            super(BaseAPIError, self).__init__(error_key + ': ' + error_text)


class WrongDataProvidedError(BaseAPIError):
    pass


class WrongCredentialsProvidedError(BaseAPIError):
    pass
