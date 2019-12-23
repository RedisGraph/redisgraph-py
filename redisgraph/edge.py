from redisgraph import Node

from .util import *

class Edge(object):
    """
    An edge connecting two nodes.
    """
    def __init__(self, src_node, relation, dest_node, edge_id=None, properties=None):
        """
        Create a new edge.
        """
        assert src_node is not None and dest_node is not None

        self.id = edge_id
        self.relation = '' or relation
        self.properties = {} or properties
        self.src_node = src_node
        self.dest_node = dest_node

    def toString(self):
        res = ""
        if self.properties:
            props = ','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items())
            res += '{' + props + '}'

        return res

    def __str__(self):
        # Source node.
        if isinstance(self.src_node, Node):
            res = str(self.src_node)
        else:
            res = '()'

        # Edge
        res += "-["
        if self.relation:
            res += ":" + self.relation
        if self.properties:
            props = ','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items())
            res += '{' + props + '}'
        res += ']->'

        # Dest node.
        if isinstance(self.dest_node, Node):
            res += str(self.dest_node)
        else:
            res += '()'

        return res

    def __eq__(self, rhs):
        # Quick positive check, if both IDs are set.
        if self.id is not None and rhs.id is not None and self.id == rhs.id:
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
