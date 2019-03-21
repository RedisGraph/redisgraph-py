from util import *

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
        res = '(' + self.src_node.alias + ')'

        # Edge
        res += "-["
        if self.relation:
            res += ":" + self.relation
        if self.properties:
            props = ','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items())
            res += '{' + props + '}'
        res += ']->'

        # Dest node.
        res += '(' + self.dest_node.alias + ')'

        return res
