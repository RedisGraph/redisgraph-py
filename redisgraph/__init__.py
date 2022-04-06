from warnings import warn
from .node import Node     # noqa
from .edge import Edge     # noqa
from .graph import Graph   # noqa
from .path import Path     # noqa

warn("Please upgrade to redis-py (https://pypi.org/project/redis/) "
"This library is deprecated, and all features have been merged into redis-py.", DeprecationWarning, stacklevel=2)
