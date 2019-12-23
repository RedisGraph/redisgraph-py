import random
import string

def random_string(length=10):
    """
    Returns a random N chracter long string.
    """
    return ''.join(random.choice(string.ascii_lowercase) for x in range(length))

def quote_string(v):
    """
    RedisGraph strings must be quoted,
    quote_string wraps given v with quotes incase
    v is a string.
    """

    if isinstance(v, bytes):
        v = v.decode()
    elif not isinstance(v, str):
        return v
    if len(v) == 0:
        return '""'

    if v[0] != '"':
        v = '"' + v

    if v[-1] != '"':
        v = v + '"'

    return v
