from redisgraph import edge
from redisgraph import node
from tests.utils import base


class TestEdge(base.TestCase):

    def test_init(self):

        with self.assertRaises(AssertionError):
            edge.Edge(None, None, None)

        with self.assertRaises(AssertionError):
            edge.Edge(node.Node(), None, None)

        with self.assertRaises(AssertionError):
            edge.Edge(None, None, node.Node())

        self.assertIsInstance(
            edge.Edge(node.Node(node_id=1), None, node.Node(node_id=2)),
            edge.Edge
        )

    def test_toString(self):
        props_result = edge.Edge(node.Node(), None, node.Node(),
                                 properties={"a": "a", "b": 10}).toString()
        self.assertEqual(props_result, '{a:"a",b:10}')

        no_props_result = edge.Edge(node.Node(), None, node.Node(),
                                    properties={}).toString()
        self.assertEqual(no_props_result, '')

    def test_stringify(self):
        john = node.Node(alias='a', label='person',
                         properties={'name': 'John Doe',
                                     'age': 33,
                                     'someArray': [1, 2, 3]})
        japan = node.Node(alias='b', label='country',
                          properties={'name': 'Japan'})
        edge_with_relation = edge.Edge(
            john, 'visited', japan, properties={'purpose': 'pleasure'})
        self.assertEqual(
            '(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})'
            '-[:visited{purpose:"pleasure"}]->'
            '(b:country{name:"Japan"})',
            str(edge_with_relation)
        )
        edge_no_relation_no_props = edge.Edge(japan, '', john)
        self.assertEqual(
            '(b:country{name:"Japan"})'
            '-[]->'
            '(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})',
            str(edge_no_relation_no_props)
        )
        edge_only_props = edge.Edge(john, '', japan,
                                    properties={'a': 'b', 'c': 3})
        self.assertEqual(
            '(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})'
            '-[{a:"b",c:3}]->'
            '(b:country{name:"Japan"})',
            str(edge_only_props)
        )

    def test_comparision(self):
        node1 = node.Node(node_id=1)
        node2 = node.Node(node_id=2)
        node3 = node.Node(node_id=3)

        edge1 = edge.Edge(node1, None, node2)
        self.assertEqual(edge1, edge.Edge(node1, None, node2))
        self.assertNotEqual(edge1, edge.Edge(node1, "bla", node2))
        self.assertNotEqual(edge1, edge.Edge(node1, None, node3))
        self.assertNotEqual(edge1, edge.Edge(node3, None, node2))
        self.assertNotEqual(edge1, edge.Edge(node2, None, node1))
        self.assertNotEqual(edge1, edge.Edge(node1, None, node2,
                            properties={"a": 10}))
