from redisgraph import edge
from redisgraph import node
from redisgraph import path
from tests.utils import base


class TestPath(base.TestCase):

    def test_init(self):
        with self.assertRaises(TypeError):
            path.Path(None, None)

        with self.assertRaises(TypeError):
            path.Path([], None)

        with self.assertRaises(TypeError):
            path.Path(None, [])

        self.assertIsInstance(path.Path([], []), path.Path)

    def test_new_empty_path(self):
        new_empty_path = path.Path.new_empty_path()
        self.assertIsInstance(new_empty_path, path.Path)
        self.assertEqual(new_empty_path._nodes, [])
        self.assertEqual(new_empty_path._edges, [])

    def test_wrong_flows(self):
        node_1 = node.Node(node_id=1)
        node_2 = node.Node(node_id=2)
        node_3 = node.Node(node_id=3)

        edge_1 = edge.Edge(node_1, None, node_2)
        edge_2 = edge.Edge(node_1, None, node_3)

        p = path.Path.new_empty_path()
        with self.assertRaises(AssertionError):
            p.add_edge(edge_1)

        p.add_node(node_1)
        with self.assertRaises(AssertionError):
            p.add_node(node_2)

        p.add_edge(edge_1)
        with self.assertRaises(AssertionError):
            p.add_edge(edge_2)

    def test_nodes_and_edges(self):
        node_1 = node.Node(node_id=1)
        node_2 = node.Node(node_id=2)
        edge_1 = edge.Edge(node_1, None, node_2)

        p = path.Path.new_empty_path()
        self.assertEqual(p.nodes(), [])
        p.add_node(node_1)
        self.assertEqual([], p.edges())
        self.assertEqual(0, p.edge_count())
        self.assertEqual([node_1], p.nodes())
        self.assertEqual(node_1, p.get_node(0))
        self.assertEqual(node_1, p.first_node())
        self.assertEqual(node_1, p.last_node())
        self.assertEqual(1, p.nodes_count())
        p.add_edge(edge_1)
        self.assertEqual([edge_1], p.edges())
        self.assertEqual(1, p.edge_count())
        self.assertEqual(edge_1, p.get_relationship(0))
        p.add_node(node_2)
        self.assertEqual([node_1, node_2], p.nodes())
        self.assertEqual(node_1, p.first_node())
        self.assertEqual(node_2, p.last_node())
        self.assertEqual(2, p.nodes_count())

    def test_compare(self):
        node_1 = node.Node(node_id=1)
        node_2 = node.Node(node_id=2)
        edge_1 = edge.Edge(node_1, None, node_2)

        self.assertEqual(path.Path.new_empty_path(),
                         path.Path.new_empty_path())
        self.assertEqual(path.Path(nodes=[node_1, node_2], edges=[edge_1]),
                         path.Path(nodes=[node_1, node_2], edges=[edge_1]))
        self.assertNotEqual(path.Path(nodes=[node_1], edges=[]),
                            path.Path(nodes=[], edges=[]))
        self.assertNotEqual(path.Path(nodes=[node_1], edges=[]),
                            path.Path(nodes=[], edges=[]))
        self.assertNotEqual(path.Path(nodes=[node_1], edges=[]),
                            path.Path(nodes=[node_2], edges=[]))
        self.assertNotEqual(path.Path(nodes=[node_1], edges=[edge_1]),
                            path.Path(nodes=[node_1], edges=[]))
        self.assertNotEqual(path.Path(nodes=[node_1], edges=[edge_1]),
                            path.Path(nodes=[node_2], edges=[edge_1]))
