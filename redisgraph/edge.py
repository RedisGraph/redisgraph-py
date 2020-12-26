from redisgraph import Node

from .util import *

class Edge:
    """
    An edge connecting two nodes.
    """
    def __init__(self, src_node, relation, dest_node, edge_id=None, properties=None):
        """
        Create a new edge.
        """
        if not (src_node and dest_node):
            # NOTE(bors-42): It makes sense to change AssertionError to
            #                ValueError here
            raise AssertionError("Both src_node & dest_node must be provided")

        self.id = edge_id
        self.relation = relation or ''
        self.properties = properties or {}
        self.src_node = src_node
        self.dest_node = dest_node

    def toString(self):
        res = ''
        if self.properties:
            props = ','.join(
                f'{key}:{quote_string(val)}'
                for key, val in sorted(self.properties.items()))
            res = f'{{{props}}}'

        return res

    def __str__(self):
        # Source node.
        res = str(self.src_node) if isinstance(self.src_node, Node) else '()'

        # Edge
        edge_relation = f':{self.relation}' if self.relation else ''
        res += f'-[{edge_relation} {self.toString()}]->'

        # Dest node.
        res += f"{self.dest_node if isinstance(self.dest_node, Node) else ''}"

        return res

    def __eq__(self, rhs):
        # Quick positive check, if both IDs are set.
        if self.id and self.id == rhs.id:
            return True

        # Source and destination nodes should match.
        if self.src_node != rhs.src_node:
            return False

        if self.dest_node != rhs.dest_node:
            return False

        # Relation should match.
        if self.relation != rhs.relation:
            return False

        # Quick check for number of properties.
        if len(self.properties) != len(rhs.properties):
            return False

        # Compare properties.
        if self.properties != rhs.properties:
            return False

        return True
