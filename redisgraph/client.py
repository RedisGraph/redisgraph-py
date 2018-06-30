import random
import string

from .query_result import QueryResult

def random_string(length=10):
    """
    Returns a random N chracter long string.
    """
    return ''.join(random.choice(string.ascii_lowercase) for x in range(length))

def quote_string(prop):
    """
    RedisGraph strings must be quoted,
    quote_string wraps given prop with quotes incase
    prop is a string.
    """
    if not isinstance(prop, str):
        return prop

    if prop[0] != '"':
        prop = '"' + prop

    if prop[-1] != '"':
        prop = prop + '"'

    return prop

class Node(object):
    """
    A node within the garph.
    """
    def __init__(self, node_id=None, alias=None, label=None, properties=None):
        """
        Create a new node
        """
        self.id = node_id
        self.alias = alias
        self.label = label
        self.properties = properties

    def __str__(self):
        return '({alias}:{label} {{{properties}}})'.format(
            alias=self.alias,
            label=self.label,
            properties=','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items()))

class Edge(object):
    """
    An edge connecting two nodes.
    """
    def __init__(self, src_node, relation, dest_node, properties=None):
        """
        Create a new edge.
        """
        assert src_node is not None and dest_node is not None

        self.relation = relation
        self.properties = properties if properties != None else {}
        self.src_node = src_node
        self.dest_node = dest_node

    def __str__(self):
        if len(self.properties) > 0:
            return '({src_alias})-[:{relation} {{{properties}}}]->({dest_alias})'.format(
                src_alias=self.src_node.alias,
                relation=self.relation,
                properties=','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items()),
                dest_alias=self.dest_node.alias)
        else:
            return '({src_alias})-[:{relation}]->({dest_alias})'.format(
                src_alias=self.src_node.alias,
                relation=self.relation,
                dest_alias=self.dest_node.alias)

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

    def query(self, q):
        """
        Executes a query against the graph.
        """
        statistics = None
        result_set = None
        response = self.redis_con.execute_command("GRAPH.QUERY", self.name, q)

        if len(response) == 1:
            statistics = response[0]
        else:
            data = response[0]
            statistics = response[1]
            result_set = [res.decode().split(',') for res in data]

        return QueryResult(result_set, statistics)

    def execution_plan(self, query):
        """
        Get the execution plan for given query.
        """
        return self.redis_con.execute_command("GRAPH.EXPLAIN", self.name, query)
