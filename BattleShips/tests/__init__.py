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

    def assertOutput(self, executable, expected_Output):
        import sys
        from StringIO import StringIO

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            executable(True)
            output = out.getvalue().strip()
            self.assertEquals(output, expected_Output)
        finally:
            sys.stdout = saved_stdout