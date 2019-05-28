import redis
import unittest
from redisgraph import *


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.r = redis.Redis(host='localhost', port=6379)

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

		# All done, remove graph.
        redis_graph.delete()

if __name__ == '__main__':
	unittest.main()
