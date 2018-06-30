from prettytable import PrettyTable


class QueryResult(object):

    LABELS_ADDED = 'Labels added'
    NODES_CREATED = 'Nodes created'
    NODES_DELETED = 'Nodes deleted'
    RELATIONSHIPS_DELETED = 'Relationships deleted'
    PROPERTIES_SET = 'Properties set'
    RELATIONSHIPS_CREATED = 'Relationships created'
    INTERNAL_EXECUTION_TIME = 'internal execution time'

    def __init__(self, result_set, statistics):
        self.result_set = result_set
        self.statistics = statistics
        self.parsed_statistics = self._retrieve_data_from_statistics(statistics)


    """Prints the data from the query response:
       1. First row result_set contains the columns names. Thus the first row in PrettyTable
          will contain the columns.
       2. The row after that will contain the data returned, or 'No Data returned' if there is none.
       3. Prints the statistics of the query.
    """
    def pretty_print(self):
        if self.result_set is not None:
            tbl = PrettyTable(self.result_set[0])
            for row in self.result_set[1:]:
                tbl.add_row(row)

            if len(self.result_set) == 1:
                tbl.add_row(['No data returned.'])

            print(str(tbl) + '\n')

        for stat in self.statistics:
            print(stat)

    def _retrieve_data_from_statistics(self, statistics):
        return {
            self.LABELS_ADDED: self._get_value(self.LABELS_ADDED, statistics),
            self.NODES_CREATED: self._get_value(self.NODES_CREATED, statistics),
            self.PROPERTIES_SET: self._get_value(self.PROPERTIES_SET, statistics),
            self.RELATIONSHIPS_CREATED: self._get_value(self.RELATIONSHIPS_CREATED, statistics),
            self.NODES_DELETED: self._get_value(self.NODES_DELETED, statistics),
            self.RELATIONSHIPS_DELETED: self._get_value(self.RELATIONSHIPS_DELETED, statistics),
            self.INTERNAL_EXECUTION_TIME: self._get_value(self.INTERNAL_EXECUTION_TIME, statistics)
        }

    @staticmethod
    def _get_value(prop, statistics):
        for stat in statistics:
            stat = stat.decode()
            if prop in stat:
                return float(stat.split(': ')[1].split(' ')[0])

        return 0

    @property
    def labels_added(self):
        return self.parsed_statistics[self.LABELS_ADDED]

    @property
    def nodes_created(self):
        return self.parsed_statistics[self.NODES_CREATED]

    @property
    def nodes_deleted(self):
        return self.parsed_statistics[self.NODES_DELETED]

    @property
    def properties_set(self):
        return self.parsed_statistics[self.PROPERTIES_SET]

    @property
    def relationships_created(self):
        return self.parsed_statistics[self.RELATIONSHIPS_CREATED]

    @property
    def relationships_deleted(self):
        return self.parsed_statistics[self.RELATIONSHIPS_DELETED]

    @property
    def run_time_ms(self):
        return self.parsed_statistics[self.INTERNAL_EXECUTION_TIME]
