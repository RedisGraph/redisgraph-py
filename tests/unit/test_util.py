
from redisgraph import util

from tests.utils import base


class TestUtils(base.TestCase):

    def test_random_string(self):
        self.assertEqual(10, len(util.random_string()))
        self.assertEqual(5, len(util.random_string(length=5)))

    def test_quote_string(self):
        self.assertEqual(util.quote_string(10), 10)
        self.assertEqual(util.quote_string("abc"), '"abc"')
        self.assertEqual(util.quote_string(""), '""')
        self.assertEqual(util.quote_string('\"'), '"\\\""')
        self.assertEqual(util.quote_string('"'), '"\\""')
        self.assertEqual(util.quote_string('a"a'), '"a\\"a"')

    def test_stringify_param_value(self):
        cases = [
            [
                "abc", '"abc"'
            ],
            [
                None, "null"
            ],
            [
                ["abc", 123, None],
                '["abc",123,null]'
            ],
            [
                {'age': 2, 'color': 'orange'},
                '{age:2,color:"orange"}'
            ],
            [
                [{'age': 2, 'color': 'orange'}, {'age': 7, 'color': 'gray'}, ],
                '[{age:2,color:"orange"},{age:7,color:"gray"}]'
            ],
        ]
        for param, expected in cases:
            observed = util.stringify_param_value(param)
            self.assertEqual(observed, expected)
