import random
import string

__all__ = ['random_string', 'quote_string', 'stringify_param_value']


def random_string(length=10):
    """
    Returns a random N character long string.
    """
    return ''.join(random.choice(string.ascii_lowercase) for x in range(length))  # nosec


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

    v = v.replace('\\', '\\\\')
    v = v.replace('"', '\\"')

    return '"{}"'.format(v)


def stringify_param_value(value):
    """
    Turn a parameter value into a string suitable for the params header of
    a Cypher command.

    You may pass any value that would be accepted by `json.dumps()`.

    Ways in which output differs from that of `str()`:
        * Strings are quoted.
        * None --> "null".
        * In dictionaries, keys are _not_ quoted.

    :param value: The parameter value to be turned into a string.
    :return: string
    """
    if isinstance(value, str):
        return quote_string(value)
    elif value is None:
        return "null"
    elif isinstance(value, (list, tuple)):
        return f'[{",".join(map(stringify_param_value, value))}]'
    elif isinstance(value, dict):
        return f'{{{",".join(f"{k}:{stringify_param_value(v)}" for k, v in value.items())}}}'
    else:
        return str(value)
