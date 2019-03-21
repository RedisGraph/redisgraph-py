from util import *
from query_result import QueryResult
class Graph(object):
    """
    Graph, collection of nodes and edges.
    """

    def __init__(self, name, redis_con):
        """
        Create a new graph.
        """
        self.name = name
        self.redis_con = redis_con
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        """
        Adds a node to the graph.
        """
        if node.alias is None:
            node.alias = random_string()
        self.nodes[node.alias] = node

    def add_edge(self, edge):
        """
        Addes an edge to the graph.
        """

        # Make sure edge both ends are in the graph
        assert self.nodes[edge.src_node.alias] is not None and self.nodes[edge.dest_node.alias] is not None
        self.edges.append(edge)

    def commit(self):
        """
        Create entire graph.
        """

        query = 'CREATE '
        for _, node in self.nodes.items():
            query += str(node) + ','

        for edge in self.edges:
            query += str(edge) + ','

        # Discard leading comma.
        if query[-1] is ',':
            query = query[:-1]

        return self.query(query)

    def flush(self):
        """
        Commit the graph and reset the edges and nodes to zero length
        """
        try:
            self.commit()
            self.nodes = {}
            self.edges = []
        except:
            print("Error flushing graph")

    def query(self, q):
        """
        Executes a query against the graph.
        """
        statistics = None
        result_set = None
        response = self.redis_con.execute_command("GRAPH.QUERY", self.name, q, "--compact")
        return QueryResult(response)

    def execution_plan(self, query):
        """
        Get the execution plan for given query.
        """
        return self.redis_con.execute_command("GRAPH.EXPLAIN", self.name, query)

    def delete(self):
        """
        Deletes graph.
        """
        return self.redis_con.execute_command("GRAPH.DELETE", self.name)
    
    def merge(self, pattern):
        """
        Merge pattern.
        """

        query = 'MERGE '
        query += str(pattern)

        return self.query(query)
