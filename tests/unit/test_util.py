
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
        self.assertEqual(util.quote_string('a"a'), '"a\\"a"')
