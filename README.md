[![PyPI version](https://badge.fury.io/py/redisgraph.svg)](https://badge.fury.io/py/redisgraph)

# redisgraph-py
RedisGraph python client


# Example: Using the Python Client

```python
import redis
from redisgraph import Node, Edge, Graph

r = redis.Redis(host='localhost', port=6379)

redis_graph = Graph('social', r)

john = Node(label='person', properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
redis_graph.add_node(john)

japan = Node(label='country', properties={'name': 'Japan'})
redis_graph.add_node(japan)

edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
redis_graph.add_edge(edge)

redis_graph.commit()

query = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)
		   RETURN p.name, p.age, v.purpose, c.name"""

result = redis_graph.query(query)

# Print resultset
result.pretty_print()

# Iterate through resultset, skip header row at position 0
for record in result.result_set[1:]:
	person_name = record[0]
	person_age = record[1]
	visit_purpose = record[2]
	country_name = record[3]


# All done, remove graph.
redis_graph.delete()
```

# Installing
```
pip install redisgraph
```
