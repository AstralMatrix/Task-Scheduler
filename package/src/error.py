class Error(Exception):
    pass


def ensure(value, e):
    if not value:
        raise e
    return
