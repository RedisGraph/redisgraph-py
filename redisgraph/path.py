from .node import Node
from .edge import Edge

class Path(object):

    def __init__(self, nodes, edges):
        assert(isinstance(nodes, list) and isinstance(edges, list))
        self.nodes = nodes
        self.edges = edges
        self.append_type = Node

    @classmethod
    def new_empty_path(cls):
        return cls([], [])

    def nodes(self):
        return self.nodes

    def edges(self):
        return self.edges

    def get_node(self, index):
        return self.nodes[index]

    def get_relationship(self, index):
        return self.edges[index]

    def first_node(self):
        return self.nodes[0]

    def last_node(self):
        return self.nodes[-1]

    def edge_count(self):
        return len(self.edges)
    
    def nodes_count(self):
        return len(self.nodes)

    def add_node(self, node):
        assert(isinstance(node, self.append_type))
        self.nodes.append(node)
        self.append_type = Edge
        return self

    def add_edge(self, edge):
        assert(isinstance(edge, self.append_type))
        self.edges.append(edge)
        self.append_type = Node
        return self

    def __eq__(self, other):
        return self.nodes == other.nodes and self.edges == other.edges
