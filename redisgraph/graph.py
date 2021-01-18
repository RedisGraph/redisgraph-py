import redis

from redisgraph.util import random_string, quote_string
from redisgraph.query_result import QueryResult
from redisgraph.exceptions import VersionMismatchException


class Graph:
    """
    Graph, collection of nodes and edges.
    """

    def __init__(self, name, redis_con):
        """
        Create a new graph.
        """
        self.name = name                 # Graph key
        self.redis_con = redis_con
        self.nodes = {}
        self.edges = []
        self._labels = []                # List of node labels.
        self._properties = []            # List of properties.
        self._relationshipTypes = []     # List of relation types.
        self.version = 0                 # Graph version

    def _clear_schema(self):
        self._labels = []
        self._properties = []
        self._relationshipTypes = []

    def _refresh_schema(self):
        self._clear_schema()
        self._refresh_labels()
        self._refresh_relations()
        self._refresh_attributes()

    def _refresh_labels(self):
        lbls = self.labels()

        # Unpack data.
        self._labels = [None] * len(lbls)
        for i, l in enumerate(lbls):
            self._labels[i] = l[0]

    def _refresh_relations(self):
        rels = self.relationshipTypes()

        # Unpack data.
        self._relationshipTypes = [None] * len(rels)
        for i, r in enumerate(rels):
            self._relationshipTypes[i] = r[0]

    def _refresh_attributes(self):
        props = self.propertyKeys()

        # Unpack data.
        self._properties = [None] * len(props)
        for i, p in enumerate(props):
            self._properties[i] = p[0]

    def get_label(self, idx):
        try:
            label = self._labels[idx]
        except IndexError:
            # Refresh labels.
            self._refresh_labels()
            label = self._labels[idx]
        return label

    def get_relation(self, idx):
        try:
            relationshipType = self._relationshipTypes[idx]
        except IndexError:
            # Refresh relationship types.
            self._refresh_relations()
            relationshipType = self._relationshipTypes[idx]
        return relationshipType

    def get_property(self, idx):
        try:
            propertie = self._properties[idx]
        except IndexError:
            # Refresh properties.
            self._refresh_attributes()
            propertie = self._properties[idx]
        return propertie

    def add_node(self, node):
        """
        Adds a node to the graph.
        """
        if node.alias is None:
            node.alias = random_string()
        self.nodes[node.alias] = node

    def add_edge(self, edge):
        """
        Adds an edge to the graph.
        """
        if not (self.nodes[edge.src_node.alias]
                and self.nodes[edge.dest_node.alias]):
            raise AssertionError("Both edge's end must be in the graph")

        self.edges.append(edge)

    def commit(self):
        """
        Create entire graph.
        """
        if len(self.nodes) == 0 and len(self.edges) == 0:
            return None

        query = 'CREATE '
        for _, node in self.nodes.items():
            query += str(node) + ','

        query += ','.join([str(edge) for edge in self.edges])

        # Discard leading comma.
        if query[-1] == ',':
            query = query[:-1]

        return self.query(query)

    def flush(self):
        """
        Commit the graph and reset the edges and nodes to zero length
        """
        self.commit()
        self.nodes = {}
        self.edges = []

    def build_params_header(self, params):
        if not isinstance(params, dict):
            raise TypeError("'params' must be a dict")
        # Header starts with "CYPHER"
        params_header = "CYPHER "
        for key, value in params.items():
            # If value is string add quotation marks.
            if isinstance(value, str):
                value = quote_string(value)
            # Value is None, replace with "null" string.
            elif value is None:
                value = "null"
            params_header += str(key) + "=" + str(value) + " "
        return params_header

    def query(self, q, params=None, timeout=None, read_only=False):
        """
        Executes a query against the graph.
        """

        # maintain original 'q'
        query = q

        # handle query parameters
        if params is not None:
            query = self.build_params_header(params) + query

        # construct query command
        # ask for compact result-set format
        # specify known graph version
        cmd = "GRAPH.RO_QUERY" if read_only else "GRAPH.QUERY"
        # command = [cmd, self.name, query, "--compact", "version", self.version]
        command = [cmd, self.name, query, "--compact"]

        # include timeout is specified
        if timeout:
            if not isinstance(timeout, int):
                raise Exception("Timeout argument must be a positive integer")
            command += ["timeout", timeout]

        # issue query
        try:
            response = self.redis_con.execute_command(*command)
            return QueryResult(self, response)
        except redis.exceptions.ResponseError as e:
            if "wrong number of arguments" in str(e):
                print("Note: RedisGraph Python requires server version 2.2.8 or above")
            raise e
        except VersionMismatchException as e:
            # client view over the graph schema is out of sync
            # set client version and refresh local schema
            self.version = e.version
            self._refresh_schema()
            # re-issue query
            return self.query(q, params, timeout, read_only)

    def _execution_plan_to_string(self, plan):
        return "\n".join(plan)

    def execution_plan(self, query, params=None):
        """
        Get the execution plan for given query,
        GRAPH.EXPLAIN returns an array of operations.
        """
        if params is not None:
            query = self.build_params_header(params) + query

        plan = self.redis_con.execute_command("GRAPH.EXPLAIN", self.name, query, query)
        return self._execution_plan_to_string(plan)

    def delete(self):
        """
        Deletes graph.
        """
        self._clear_schema()
        return self.redis_con.execute_command("GRAPH.DELETE", self.name)

    def merge(self, pattern):
        """
        Merge pattern.
        """

        query = 'MERGE '
        query += str(pattern)

        return self.query(query)

    # Procedures.
    def call_procedure(self, procedure, *args, read_only=False, **kwagrs):
        args = [quote_string(arg) for arg in args]
        q = 'CALL %s(%s)' % (procedure, ','.join(args))

        y = kwagrs.get('y', None)
        if y:
            q += ' YIELD %s' % ','.join(y)

        return self.query(q, read_only=read_only)

    def labels(self):
        return self.call_procedure("db.labels", read_only=True).result_set

    def relationshipTypes(self):
        return self.call_procedure("db.relationshipTypes", read_only=True).result_set

    def propertyKeys(self):
        return self.call_procedure("db.propertyKeys", read_only=True).result_set
