import redis
import unittest
from redisgraph import *


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def test_graph_creation(self):
        redis_graph = Graph('social', self.r)
        
        john = Node(label='person', properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
        redis_graph.add_node(john)
        japan = Node(label='country', properties={'name': 'Japan'})
        
        redis_graph.add_node(japan)
        edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
        redis_graph.add_edge(edge)
        
        redis_graph.commit()
        
        query = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)
				   RETURN p, v, c"""
        
        result = redis_graph.query(query)
        
        person = result.result_set[0][0]
        visit = result.result_set[0][1]
        country = result.result_set[0][2]
        
        self.assertEqual(person, john)
        self.assertEqual(visit.properties, edge.properties)
        self.assertEqual(country, japan)

        query = """RETURN [1, 2.3, "4", true, false, null]"""
        result = redis_graph.query(query)
        self.assertEqual([1, 2.3, "4", True, False, None], result.result_set[0][0])

		# All done, remove graph.
        redis_graph.delete()

    def test_array_functions(self):
        redis_graph = Graph('social', self.r)

        query = """CREATE (p:person{name:'a',age:32, array:[0,1,2]})"""
        redis_graph.query(query)

        query = """CREATE (p:person{name:'b',age:30, array:[3,4,5]})"""
        redis_graph.query(query)

        query = """WITH [0,1,2] as x return x"""
        result = redis_graph.query(query)
        self.assertEqual([0, 1, 2], result.result_set[0][0])

        query = """MATCH(n) return collect(n) as x"""
        result = redis_graph.query(query)

        a = Node(label='person', properties={'name': 'a', 'age': 32, 'array': [0, 1, 2]})
        b = Node(label='person', properties={'name': 'b', 'age': 30, 'array': [3, 4, 5]})

        self.assertEqual([a, b], result.result_set[0][0])


        # All done, remove graph.
        redis_graph.delete()


    def test_path(self):
        redis_graph = Graph('social', self.r)

        node0 = Node(node_id=0, label="L1")
        node1 = Node(node_id=1, label="L1")
        node2 = Node(node_id=2, label="L1")
        edge01 = Edge(node0, "R1", node1, edge_id=0, properties={'value': 1})
        edge12 = Edge(node1, "R1", node2, edge_id=1, properties={'value': 2})

        redis_graph.add_node(node0)
        redis_graph.add_node(node1)
        redis_graph.add_node(node2)
        redis_graph.add_edge(edge01)
        redis_graph.add_edge(edge12)

        redis_graph.flush()

        path01 = Path.new_empty_path().add_node(node0).add_edge(edge01).add_node(node1)
        path12 = Path.new_empty_path().add_node(node1).add_edge(edge12).add_node(node2)
        expected_results = [[path01], [path12]]

        query = "MATCH p=(:L1)-[:R1]->(:L1) RETURN p"
        result = redis_graph.query(query)
        self.assertEqual(expected_results, result.result_set)

        # All done, remove graph.
        redis_graph.delete()

    def test_param(self):
        redis_graph = Graph('params', self.r)

        params = [1, 2.3, "str", True, False, None, [0, 1, 2]]
        query = "RETURN $param"
        for param in params:
            result = redis_graph.query(query, {'param': param})
            expected_results = [[param]]
            self.assertEqual(expected_results, result.result_set)

        # All done, remove graph.
        redis_graph.delete()

    def test_index_response(self):
        redis_graph = Graph('social', self.r)

        result_set = redis_graph.query("CREATE INDEX ON :person(age)")
        self.assertEqual(1, result_set.indices_created)

        result_set = redis_graph.query("CREATE INDEX ON :person(age)")
        self.assertEqual(0, result_set.indices_created)

        result_set = redis_graph.query("DROP INDEX ON :person(age)")
        self.assertEqual(1, result_set.indices_deleted)

        try:
            result_set = redis_graph.query("DROP INDEX ON :person(age)")
        except redis.exceptions.ResponseError as e:
            self.assertEqual(e.__str__(), "Unable to drop index on :person(age): no such index.")

        redis_graph.delete()

if __name__ == '__main__':
	unittest.main()
