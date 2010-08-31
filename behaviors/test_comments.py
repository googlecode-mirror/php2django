import unittest
import comments
from utils import string_to_list, side_by_side

class TestCommentUnconvertedLines(unittest.TestCase):
    #TODO: Oops. Forgot to write a test for this.
    pass

class TestStandardizeComments(unittest.TestCase):
    def _test(self, source, expected):
        got, ignore = comments.standardize_comments(source, [])
        msg = side_by_side(got, expected)
        self.assertEqual(got, expected, msg)

    def test_code_in_string(self):
        self._test("echo 'if (0) { echo 1; }';",
                   ["echo 'if (0) { echo 1; }';", ])

    def test_code_in_comments(self):
        self._test("echo 1; /* if (0) { echo 1; } */",
                   ["# if (0) { echo 1; }", "echo 1;", ])

    def test_comment_after_code(self):
        self._test("echo 1; /* comment */",
                   ["# comment", "echo 1;", ])

    def test_comment_before_code(self):
        self._test("/* comment */ echo 1;",
                   ["# comment", "echo 1;",])


    def test_comment_line(self):
        source = string_to_list("""
            <?php
            /* this is a comment line */
            echo 'this is code';
            /* this is another comment line */
            >?""")
        expected = string_to_list("""
            <?php
            # this is a comment line
            echo 'this is code';
            # this is another comment line
            >?""")
        self._test(source, expected)

    def test_comment_block(self):
        source = string_to_list("""
            <?php
            /* this is a comment block
             * with a second line
             */
            echo 'this is code';
            >?""")
        expected = string_to_list("""
            <?php
            # this is a comment block
            # with a second line
            echo 'this is code';
            >?""")
        self._test(source, expected)

if __name__ == "__main__":
    unittest.main()