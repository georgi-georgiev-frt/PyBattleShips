import unittest
import re


class BattleShipsTest(unittest.TestCase):
    """
    Extending TestCase functionality
    """

    def assertMatch(self, pattern, string, msg=None):
        """
        Throw an exception if the regular expression pattern is not matched
        :param pattern: string
        :param string: string
        :param msg: string
        :return:
        """
        # Not part of unittest, but convenient for some koans tests
        m = re.search(pattern, string)
        if not m or not m.group(0):
            raise self.failureException, \
                (msg or '{0!r} does not match {1!r}'.format(pattern, string))

    def assertOutput(self, executable, expected_output, msg=None):
        """
        Assert executing executable will output expected output
        :param executable: function
        :param expected_output: string
        :param msg: string|None
        :return:
        """
        import sys
        from StringIO import StringIO

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            executable(True)
            output = out.getvalue().strip()
            self.assertEquals(output, expected_output, msg)
        finally:
            sys.stdout = saved_stdout