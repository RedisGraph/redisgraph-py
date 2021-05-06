from .node import Node
from .edge import Edge


class Path:
    def __init__(self, nodes, edges):
        if not (isinstance(nodes, list) and isinstance(edges, list)):
            raise TypeError("nodes and edges must be list")

        self._nodes = nodes
        self._edges = edges
        self.append_type = Node

    @classmethod
    def new_empty_path(cls):
        return cls([], [])

    def nodes(self):
        return self._nodes

    def edges(self):
        return self._edges

    def get_node(self, index):
        return self._nodes[index]

    def get_relationship(self, index):
        return self._edges[index]

    def first_node(self):
        return self._nodes[0]

    def last_node(self):
        return self._nodes[-1]

    def edge_count(self):
        return len(self._edges)

    def nodes_count(self):
        return len(self._nodes)

    def add_node(self, node):
        if not isinstance(node, self.append_type):
            raise AssertionError("Add Edge before adding Node")
        self._nodes.append(node)
        self.append_type = Edge
        return self

    def add_edge(self, edge):
        if not isinstance(edge, self.append_type):
            raise AssertionError("Add Node before adding Edge")
        self._edges.append(edge)
        self.append_type = Node
        return self

    def __eq__(self, other):
        return self.nodes() == other.nodes() and self.edges() == other.edges()

    def __str__(self):
        res = ""
        edge_count = self.edge_count()
        for i in range(edge_count):
            node_id = self.get_node(i).id
            res += f"({node_id})"
            edge = self.get_relationship(i)
            if edge.src_node == node_id:
                res = f"{res}-[{edge.id}]->"
            else:
                res = f"{res}<-[{edge.id}]-"

        return f'<{res}({self.get_node(edge_count).id})>'
