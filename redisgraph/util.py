import random
import string

def random_string(length=10):
    """
    Returns a random N chracter long string.
    """
    return ''.join(random.choice(string.ascii_lowercase) for x in range(length))

def quote_string(prop):
    """
    RedisGraph strings must be quoted,
    quote_string wraps given prop with quotes incase
    prop is a string.
    """
    if not isinstance(prop, str):
        return prop

    if prop[0] != '"':
        prop = '"' + prop

    if prop[-1] != '"':
        prop = prop + '"'

    return prop
