import unittest
import re


class BattleShipsTest(unittest.TestCase):

    def assertMatch(self, pattern, string, msg=None):
        """
        Throw an exception if the regular expresson pattern is matched
        """
        # Not part of unittest, but convenient for some koans tests
        m = re.search(pattern, string)
        if not m or not m.group(0):
            raise self.failureException, \
                (msg or '{0!r} does not match {1!r}'.format(pattern, string))