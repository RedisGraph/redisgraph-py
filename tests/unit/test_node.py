from redisgraph import node
from tests.utils import base


class TestNode(base.TestCase):

    def setUp(self):
        super().setUp()
        self.no_args = node.Node()
        self.no_props = node.Node(node_id=1, alias="alias", label="l")
        self.props_only = node.Node(properties={"a": "a", "b": 10})
        self.no_label = node.Node(node_id=1, alias="alias",
                                  properties={"a": "a"})

    def test_toString(self):
        self.assertEqual(self.no_args.toString(), "")
        self.assertEqual(self.no_props.toString(), "")
        self.assertEqual(self.props_only.toString(), '{a:"a",b:10}')
        self.assertEqual(self.no_label.toString(), '{a:"a"}')

    def test_stringify(self):
        self.assertEqual(str(self.no_args), "()")
        self.assertEqual(str(self.no_props), "(alias:l)")
        self.assertEqual(str(self.props_only), '({a:"a",b:10})')
        self.assertEqual(str(self.no_label), '(alias{a:"a"})')

    def test_comparision(self):

        self.assertEqual(node.Node(), node.Node())
        self.assertEqual(node.Node(node_id=1), node.Node(node_id=1))
        self.assertNotEqual(node.Node(node_id=1), node.Node(node_id=2))

        self.assertEqual(node.Node(node_id=1, alias="a"),
                         node.Node(node_id=1, alias="b"))

        self.assertEqual(node.Node(node_id=1, alias="a"),
                         node.Node(node_id=1, alias="a"))

        self.assertEqual(node.Node(node_id=1, label="a"),
                         node.Node(node_id=1, label="a"))
        self.assertNotEqual(node.Node(node_id=1, label="a"),
                            node.Node(node_id=1, label="b"))

        self.assertEqual(node.Node(node_id=1, alias="a", label="l"),
                         node.Node(node_id=1, alias="a", label="l"))

        self.assertNotEqual(node.Node(alias="a", label="l"),
                            node.Node(alias="a", label="l1"))

        self.assertEqual(node.Node(properties={"a": 10}),
                         node.Node(properties={"a": 10}))
        self.assertNotEqual(node.Node(), node.Node(properties={"a": 10}))
