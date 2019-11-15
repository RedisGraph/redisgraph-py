[![license](https://img.shields.io/github/license/RedisGraph/redisgraph-py.svg)](https://github.com/RedisGraph/redisgraph-py)
[![CircleCI](https://circleci.com/gh/RedisGraph/redisgraph-py/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGraph/redisgraph-py/tree/master)
[![PyPI version](https://badge.fury.io/py/redisgraph.svg)](https://badge.fury.io/py/redisgraph)
[![GitHub issues](https://img.shields.io/github/release/RedisGraph/redisgraph-py.svg)](https://github.com/RedisGraph/redisgraph-py/releases/latest)
[![Codecov](https://codecov.io/gh/RedisGraph/redisgraph-py/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisGraph/redisgraph-py)

[![Mailing List](https://img.shields.io/badge/Mailing%20List-RedisGraph-blue)](https://groups.google.com/forum/#!forum/redisgraph)
[![Gitter](https://badges.gitter.im/RedisLabs/RedisGraph.svg)](https://gitter.im/RedisLabs/RedisGraph?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


# redisgraph-py
RedisGraph python client


# Example: Using the Python Client

```python
import redis
from redisgraph import Node, Edge, Graph, Path

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

# Use parameters
params = {'purpose':"pleasure"}
query = """MATCH (p:person)-[v:visited {purpose:$purpose}]->(c:country)
		   RETURN p.name, p.age, v.purpose, c.name"""

result = redis_graph.query(query, params)

# Print resultset
result.pretty_print()


# Iterate through resultset
for record in result.result_set:
	person_name = record[0]
	person_age = record[1]
	visit_purpose = record[2]
	country_name = record[3]
	
query = """MATCH p = (:person)-[:visited {purpose:"pleasure"}]->(:country) RETURN p"""

result = redis_graph.query(query)

# Iterate through resultset
for record in result.result_set:
    path = record[0]
    print(path)


# All done, remove graph.
redis_graph.delete()
```

# Installing

### Install official release

```
pip install redisgraph
```
### Install latest release (Aligned with RedisGraph master)

```
pip install git+https://github.com/RedisGraph/redisgraph-py.git@master
```
