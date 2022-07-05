class SessionLoadError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class WrongCredentials(Exception):
    pass


class RefreshExpiredError(Exception):
    pass
