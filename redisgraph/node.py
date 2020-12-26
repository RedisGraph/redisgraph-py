from .util import *

class Node:
    """
    A node within the garph.
    """
    def __init__(self, node_id=None, alias=None, label=None, properties={}):
        """
        Create a new node
        """
        self.id = node_id
        self.alias = alias
        self.label = label
        self.properties = properties

    def toString(self):
        res = ''
        if self.properties:
            props = ','.join(
                f'{key}:{quote_string(val)}'
                for key, val in sorted(self.properties.items()))
            res = f'{{{props}}}'

        return res

    def __str__(self):
        label = f':{self.label}' if label else ''
        return f'({self.alias or ""}{label} {self.toString()})'

    def __eq__(self, rhs):
        # Quick positive check, if both IDs are set.
        if self.id and self.id == rhs.id:
            return True

        # Label should match.
        if self.label != rhs.label:
            return False

        # Quick check for number of properties.
        if len(self.properties) != len(rhs.properties):
            return False

        # Compare properties.
        if self.properties != rhs.properties:
            return False

        return True
