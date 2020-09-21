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

        query = """WITH [0,1,2] as x return x"""
        result = redis_graph.query(query)
        self.assertEqual([0, 1, 2], result.result_set[0][0])

        query = """MATCH(n) return collect(n)"""
        result = redis_graph.query(query)

        a = Node(node_id=0, label='person', properties={'name': 'a', 'age': 32, 'array': [0, 1, 2]})

        self.assertEqual([a], result.result_set[0][0])

        # All done, remove graph.
        redis_graph.delete()

    def test_path(self):
        redis_graph = Graph('social', self.r)

        node0 = Node(node_id=0, label="L1")
        node1 = Node(node_id=1, label="L1")
        edge01 = Edge(node0, "R1", node1, edge_id=0, properties={'value': 1})

        redis_graph.add_node(node0)
        redis_graph.add_node(node1)
        redis_graph.add_edge(edge01)

        redis_graph.flush()

        path01 = Path.new_empty_path().add_node(node0).add_edge(edge01).add_node(node1)
        expected_results = [[path01]]

        query = "MATCH p=(:L1)-[:R1]->(:L1) RETURN p ORDER BY p"
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

    def test_stringify_query_result(self):
        redis_graph = Graph('stringify', self.r)

        john = Node(alias='a', label='person',
                    properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
        redis_graph.add_node(john)
        japan = Node(alias='b', label='country', properties={'name': 'Japan'})

        redis_graph.add_node(japan)
        edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
        redis_graph.add_edge(edge)

        self.assertEqual(str(john),
                         """(a:person{age:33,gender:"male",name:"John Doe",status:"single"})""")
        self.assertEqual(str(edge),
                         """(a:person{age:33,gender:"male",name:"John Doe",status:"single"})""" +
                         """-[:visited{purpose:"pleasure"}]->""" +
                         """(b:country{name:"Japan"})""")
        self.assertEqual(str(japan), """(b:country{name:"Japan"})""")

        redis_graph.commit()

        query = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)
                RETURN p, v, c"""

        result = redis_graph.query(query)
        person = result.result_set[0][0]
        visit = result.result_set[0][1]
        country = result.result_set[0][2]

        self.assertEqual(str(person), """(:person{age:33,gender:"male",name:"John Doe",status:"single"})""")
        self.assertEqual(str(visit), """()-[:visited{purpose:"pleasure"}]->()""")
        self.assertEqual(str(country), """(:country{name:"Japan"})""")

        redis_graph.delete()

    def test_optional_match(self):
        redis_graph = Graph('optional', self.r)

        # Build a graph of form (a)-[R]->(b)
        node0 = Node(node_id=0, label="L1", properties={'value': 'a'})
        node1 = Node(node_id=1, label="L1", properties={'value': 'b'})

        edge01 = Edge(node0, "R", node1, edge_id=0)

        redis_graph.add_node(node0)
        redis_graph.add_node(node1)
        redis_graph.add_edge(edge01)

        redis_graph.flush()

        # Issue a query that collects all outgoing edges from both nodes (the second has none).
        query = """MATCH (a) OPTIONAL MATCH (a)-[e]->(b) RETURN a, e, b ORDER BY a.value"""
        expected_results = [[node0, edge01, node1],
                            [node1, None, None]]

        result = redis_graph.query(query)
        self.assertEqual(expected_results, result.result_set)

        redis_graph.delete()

    def test_cached_execution(self):
        redis_graph = Graph('cached', self.r)
        redis_graph.query("CREATE ()")
        
        uncached_result = redis_graph.query("MATCH (n) RETURN n, $param", {'param': [0]})
        self.assertFalse(uncached_result.cached_execution)
        
        # loop to make sure the query is cached on each thread on server
        for x in range(0, 64): 
            cached_result = redis_graph.query("MATCH (n) RETURN n, $param", {'param': [0]})
            self.assertEqual(uncached_result.result_set, cached_result.result_set)

        # should be cached on all threads by now
        self.assertTrue(cached_result.cached_execution)
        
        redis_graph.delete()
        
        
    def test_execution_plan(self):
        redis_graph = Graph('execution_plan', self.r)
        create_query = """CREATE (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}), 
        (:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'}), 
        (:Rider {name:'Andrea Dovizioso'})-[:rides]->(:Team {name:'Ducati'})"""
        redis_graph.query(create_query)
        
        result = redis_graph.execution_plan("MATCH (r:Rider)-[:rides]->(t:Team) WHERE t.name = $name RETURN r.name, t.name, $params", {'name': 'Yehuda'})
        expected = "Results\n    Project\n        Conditional Traverse | (t:Team)->(r:Rider)\n            Filter\n                Node By Label Scan | (t:Team)"
        self.assertEqual(result, expected)
        
        redis_graph.delete()

    def test_query_timeout(self):
        redis_graph = Graph('timeout', self.r)
        # Build a sample graph with 1000 nodes.
        redis_graph.query("UNWIND range(0,1000) as val CREATE ({v: val})")
        # Issue a long-running query with a 1-millisecond timeout.
        try:
            redis_graph.query("MATCH (a), (b), (c), (d) RETURN *", timeout=1)
            assert(False)
        except redis.exceptions.ResponseError as e:
            assert("Query timed out" in e.args)
            # Expecting an error.
            pass

        try:
            redis_graph.query("RETURN 1", timeout="str")
            assert(False)
        except Exception as e:
            assert("Timeout argument must be a positive integer" in e.args)
            # Expecting an error.
            pass

if __name__ == '__main__':
    unittest.main()
