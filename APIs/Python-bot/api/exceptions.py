class InvalidHostError(Exception):
    pass


class BaseAPIError(Exception):
    def __init__(self, error_key, error_text):
        super(BaseAPIError, self).__init__(error_key + ': ' + error_text)
