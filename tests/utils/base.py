import unittest

import testtools
import mock


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        # NOTE(boris-42): Show all differences in complex objects
        self.maxDiff = None
        # NOTE(boris-42): Stop all mocks, to avoid hanging tests
        self.addCleanup(mock.patch.stopall)

    # NOTE(boris-42): testtools have old version of assertRaises
    #                 which doesn't support usage with "with" context.
    assertRaises = unittest.TestCase.assertRaises
