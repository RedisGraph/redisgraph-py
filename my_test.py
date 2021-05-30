import redis
from redisgraph import Node, Edge, Graph, Path

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379)

    redis_graph = Graph('social', r)

    Charlie = Node(label='Person', properties={'name': 'Charlie Sheen'})
    Michael = Node(label='Person', properties={'name': 'Michael Douglas'})
    Tamara = Node(label='Person', properties={'name': 'Tamara Tunie'})
    redis_graph.add_node(Charlie)
    redis_graph.add_node(Michael)
    redis_graph.add_node(Tamara)

    WallStreet = Node(label='movie', properties={'name': 'Wall Street'})
    redis_graph.add_node(WallStreet)

    edge = Edge(Charlie, 'ACTED_IN', WallStreet)
    redis_graph.add_edge(edge)
    edge = Edge(Tamara, 'ACTED_IN', WallStreet)
    redis_graph.add_edge(edge)

    redis_graph.commit()

    query = """MATCH (movie:Movie { name: 'Wall Street' }) 
    MERGE (person {name: 'Charlie Sheen'})-[:ACTED_IN]->(movie) 
    ON MATCH SET person.first_role = movie.name"""

    result = redis_graph.query(query)

    # Print result-set
    result.pretty_print()
    #print(result.result_set)

    #print("worked")

    redis_graph.delete()
