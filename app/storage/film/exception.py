class FilmError(Exception):
    """
    Film related error
    """


class AlreadyExistFilmError(FilmError):
    """
    Film already exists error
    """
