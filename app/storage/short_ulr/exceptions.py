class BaseShortUrlError(Exception):
    """
    Base exception for short url error
    """


class AlreadyExistsShortUrlError(BaseShortUrlError):
    """
    Short url already exists error
    """
