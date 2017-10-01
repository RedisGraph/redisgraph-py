import redis
import random
import string
from prettytable import PrettyTable

def random_string(length=10):
    """
    Returns a random N chracter long string.
    """
    return ''.join(random.choice(string.lowercase) for x in range(length))

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
            properties=','.join(key+':'+str(val) for key, val in self.properties.iteritems()))

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
                properties=','.join(key+':'+str(val) for key, val in self.properties.iteritems()),
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

    class QueryResult(object):
        def __init__(self, result_set, statistics):
            self.result_set = result_set
            self.statistics = statistics

        """Prints the data from the query response:
           1. First row result_set contains the columns names. Thus the first row in PrettyTable
              will contain the columns.
           2. The row after that will contain the data returned, or 'No Data returned' if there is none.
           3. Prints the statistics of the query.
        """
        def pretty_print(self):
            tbl = PrettyTable(self.result_set[0])
            for row in self.result_set[1:]:
                tbl.add_row(row)

            if len(self.result_set) == 1:
                tbl.add_row(['No data returned.'])

            print(str(tbl) + '\n')

            for stat in self.statistics:
                print(stat)

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
        for _, node in self.nodes.iteritems():
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
        response = self.redis_con.execute_command("GRAPH.QUERY", self.name, q)
        data = response[0]
        statistics = response[1]
        result_set = [res.split(',') for res in data]
        return self.QueryResult(result_set, statistics)

    def execution_plan(self, query):
        """
        Get the execution plan for given query.
        """
        return self.redis_con.execute_command("GRAPH.EXPLAIN", self.name, query)
