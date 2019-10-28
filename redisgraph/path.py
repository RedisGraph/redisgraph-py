
class Path(object):

    def __init__(self, nodes, relationships):
        self.nodes = nodes
        self.relationships = relationships

    def nodes(self):
        return self.nodes

    def relationships(self):
        return self.relationships

    def get_node(self, index):
        return self.nodes[index]

    def get_relationship(self, index):
        return self.relationships[index]

    def first_node(self):
        return self.nodes[0]

    def last_node(self):
        return self.nodes[-1]

    def __eq__(self, other):
        return self.nodes == other.nodes and self.relationships == other.relationships
