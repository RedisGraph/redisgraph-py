from .node import Node
from .edge import Edge
from prettytable import PrettyTable

class ResultSetColumnTypes(object):
    COLUMN_UNKNOWN = 0
    COLUMN_SCALAR = 1
    COLUMN_NODE = 2
    COLUMN_RELATION = 3

class ResultSetScalarTypes(object):
    PROPERTY_UNKNOWN = 0
    PROPERTY_NULL = 1
    PROPERTY_STRING = 2
    PROPERTY_INTEGER = 3
    PROPERTY_BOOLEAN = 4
    PROPERTY_DOUBLE = 5

class QueryResult(object):
    LABELS_ADDED = 'Labels added'
    NODES_CREATED = 'Nodes created'
    NODES_DELETED = 'Nodes deleted'
    RELATIONSHIPS_DELETED = 'Relationships deleted'
    PROPERTIES_SET = 'Properties set'
    RELATIONSHIPS_CREATED = 'Relationships created'
    INTERNAL_EXECUTION_TIME = 'internal execution time'

    def __init__(self, graph, response):
        self.graph = graph
        self.header = []
        self.result_set = []

        if len(response) is 1:
            self.parse_statistics(response[0])
        else:
            self.parse_results(response)
            self.parse_statistics(response[-1]) # Last element.

    def parse_results(self, raw_result_set):
        self.header = self.parse_header(raw_result_set)
        
        # Empty header.
        if len(self.header) == 0:
            return

        self.result_set = self.parse_records(raw_result_set)

    def parse_statistics(self, raw_statistics):
        self.statistics = {}

        stats = [self.LABELS_ADDED, self.NODES_CREATED, self.PROPERTIES_SET, self.RELATIONSHIPS_CREATED, self.NODES_DELETED, self.RELATIONSHIPS_DELETED, self.INTERNAL_EXECUTION_TIME]
        for s in stats:
            v = self._get_value(s, raw_statistics)
            if v is not None:
                self.statistics[s] = v

    def parse_header(self, raw_result_set):
        # An array of column name/column type pairs.
        header = raw_result_set[0]
        return header

    def parse_records(self, raw_result_set):
        records = []
        result_set = raw_result_set[1]
        for row in result_set:
            record = []
            for idx, cell in enumerate(row):
                if self.header[idx][0] == ResultSetColumnTypes.COLUMN_SCALAR:
                    record.append(self.parse_scalar(cell))
                elif self.header[idx][0] == ResultSetColumnTypes.COLUMN_NODE:
                    record.append(self.parse_node(cell))
                elif self.header[idx][0] == ResultSetColumnTypes.COLUMN_RELATION:
                    record.append(self.parse_edge(cell))
                else:
                    print("Unknown column type.\n")
            records.append(record)

        return records

    def parse_entity_properties(self, props):
        # [[name, value type, value] X N]
        properties = {}
        for prop in props:
            prop_name =  self.graph.get_property(prop[0])
            prop_value = self.parse_scalar(prop[1:])
            properties[prop_name] = prop_value

        return properties

    def parse_node(self, cell):
        # Node ID (integer),
        # [label string offset (integer)],
        # [[name, value type, value] X N]

        node_id = int(cell[0])
        label = None
        if len(cell[1]) != 0:
            label = self.graph.get_label(cell[1][0])
        properties = self.parse_entity_properties(cell[2])
        return Node(node_id=node_id, label=label, properties=properties)

    def parse_edge(self, cell):
        # Edge ID (integer),
        # reltype string offset (integer),
        # src node ID offset (integer),
        # dest node ID offset (integer),
        # [[name, value, value type] X N]

        edge_id = float(cell[0])
        relation = self.graph.get_relation(cell[1])
        src_node_id = float(cell[2])
        dest_node_id = float(cell[3])
        properties = self.parse_entity_properties(cell[4])
        return Edge(src_node_id, relation, dest_node_id, properties=properties)

    def parse_scalar(self, cell):
        scalar_type = int(cell[0])
        value = cell[1]

        if scalar_type == ResultSetScalarTypes.PROPERTY_NULL:
            scalar = None

        elif scalar_type == ResultSetScalarTypes.PROPERTY_STRING:
            scalar = str(value)
        
        elif scalar_type == ResultSetScalarTypes.PROPERTY_INTEGER:
            scalar = int(value)

        elif scalar_type == ResultSetScalarTypes.PROPERTY_BOOLEAN:
            if value == "true":
                scalar = True
            elif value == "false":
                scalar = False
            else:
                print("Unknown boolean type\n")

        elif scalar_type == ResultSetScalarTypes.PROPERTY_DOUBLE:
            scalar = float(value)

        elif scalar_type == ResultSetScalarTypes.PROPERTY_UNKNOWN:
            print("Unknown scalar type\n")

        return scalar

    """Prints the data from the query response:
       1. First row result_set contains the columns names. Thus the first row in PrettyTable
          will contain the columns.
       2. The row after that will contain the data returned, or 'No Data returned' if there is none.
       3. Prints the statistics of the query.
    """
    def pretty_print(self):
        if not self.is_empty():
            header = [col[1] for col in self.header]
            tbl = PrettyTable(header)

            for row in self.result_set:
                record = []
                for idx, cell in enumerate(row):
                    if type(cell) is Node:
                        record.append(cell.toString())
                    elif type(cell) is Edge:
                        record.append(cell.toString())
                    else:
                        record.append(cell)
                tbl.add_row(record)

            if len(self.result_set) == 0:
                tbl.add_row(['No data returned.'])

            print(str(tbl) + '\n')

        for stat in self.statistics:
            print("%s %s" %(stat, self.statistics[stat]))

    def is_empty(self):
        return len(self.result_set) == 0

    @staticmethod
    def _get_value(prop, statistics):
        for stat in statistics:
            if isinstance(stat, bytes):
                stat = stat.decode()
            if prop in stat:
                return float(stat.split(': ')[1].split(' ')[0])

        return None

    def _get_stat(self, stat):
        return self.statistics[stat] if stat in self.statistics else 0

    @property
    def labels_added(self):        
        return self._get_stat(self.LABELS_ADDED)

    @property
    def nodes_created(self):
        return self._get_stat(self.NODES_CREATED)

    @property
    def nodes_deleted(self):
        return self._get_stat(self.NODES_DELETED)

    @property
    def properties_set(self):
        return self._get_stat(self.PROPERTIES_SET)

    @property
    def relationships_created(self):
        return self._get_stat(self.RELATIONSHIPS_CREATED)

    @property
    def relationships_deleted(self):
        return self._get_stat(self.RELATIONSHIPS_DELETED)

    @property
    def run_time_ms(self):
        return self._get_stat(self.INTERNAL_EXECUTION_TIME)

