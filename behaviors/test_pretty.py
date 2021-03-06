import unittest
import pretty
from utils import string_to_list, side_by_side

class TestStripPhpNewlines(unittest.TestCase):
    def test_strip_newlines(self):
        source = [
            "<?php\n",
            "/* This\n",
            "   is\n",
            "   a\n",
            "   test. */\n",
            "?>"
        ]
        expected = string_to_list("""
            <?php
            /* This
               is
               a
               test. */
            ?>""")
        got, ignore = pretty.strip_php_newlines(source, [])
        self.assertEqual(got, expected)

class TestSplitPhpLine(unittest.TestCase):
    """ Tests the _split_php_line function. """
    def _test(self, source, expected):
        got = pretty._split_php_line(source)
        self.assertEqual(got, expected)

    def test_nothing(self):
        self._test("", [])

    def test_simple(self):
        self._test("echo 'hi';", ["echo 'hi';"])

    def test_2_statements(self):
        self._test("echo 'hi'; echo 'bye';", ["echo 'hi';", "echo 'bye';"])

    def test_if_statement(self):
        self._test("if (1) { echo 'yep'; }", ["if (1) {", "echo 'yep';", "}"])

    def test_if_else_statement(self):
        self._test("if (1) { echo 'yep'; } else { echo 'nope'; }",
                   ["if (1) {", "echo 'yep';", "}",
                    "else {", "echo 'nope';", "}" ])

    def test_case_statement(self):
        self._test("switch ($i) { case 0: echo 'zero'; break; case 1: echo 'one'; break; }",
                   ["switch ($i) {",
                    "case 0:",
                    "echo 'zero';",
                    "break;",
                    "case 1:",
                    "echo 'one';",
                    "break;",
                    "}"])

class TestConsolidatePhp(unittest.TestCase):
    def _test(self, source, expected):
        got, ignore = pretty.consolidate_php(source, [])
        msg = side_by_side(got, expected)
        self.assertEqual(got, expected, msg)

    def test_semicolon_ending(self):
        source = string_to_list("""
            <?php
            echo "This " . "is " .
                 "a " . "test.";
            ?>""")
        expected = string_to_list("""
            <?php
            echo "This " . "is " . "a " . "test.";
            ?>""")
        self._test(source, expected)

    def test_open_brace_ending(self):
        source = string_to_list("""
            <?php
            if (true &&
                false) {
                echo "Impossible!";
            }
            ?>""")
        expected = string_to_list("""
            <?php
            if (true && false) {
                echo "Impossible!";
            }
            ?>""")
        self._test(source, expected)

    def test_close_brace_ending(self):
        source = string_to_list("""
            <?php
            if (true && false) {
                echo "Impossible!";
            } else {
                echo "Right on.";
            }
            ?>""")
        expected = string_to_list("""
            <?php
            if (true && false) {
                echo "Impossible!";
            }
            else {
                echo "Right on.";
            }
            ?>""")
        self._test(source, expected)

    def test_switch_statement(self):
        source = string_to_list("""
            <?php
            switch ($i) {
                case 0: echo "i equals 0"; break;
                case 1: echo "i equals 1"; break;
                case 2: echo "i equals 2"; break;
            }
            ?>""")
        expected = string_to_list("""
            <?php
            switch ($i) {
                case 0:
                    echo "i equals 0";
                    break;
                case 1:
                    echo "i equals 1";
                    break;
                case 2:
                    echo "i equals 2";
                    break;
            }
            ?>""")
        self._test(source, expected)

    def test_break_apart_multiple(self):
        #TODO: This isn't working! Debug this test!
        source = string_to_list(
            '<?php switch ($i) { '
            'case 0: echo "i equals 0"; break; '
            'case 1: echo "i equals 1"; break; '
            'case 2: echo "i equals 2"; break; '
            '} '
            'if (true) { echo "True"; } else { echo "False"; }'
            '?>')
        expected = string_to_list("""
            <?php
            switch ($i) {
                case 0:
                    echo "i equals 0";
                    break;
                case 1:
                    echo "i equals 1";
                    break;
                case 2:
                    echo "i equals 2";
                    break;
            }
            if (true) {
                echo "True";
            }
            else {
                echo "False";
            }
            ?>""")
        self._test(source, expected)

    def test_reformat_indentation(self):
        source = string_to_list("""
            <?php
            if (true) {
             if (false) {
              if (true) {
                echo "Nevermind.";
            }}}
            ?>""")
        expected = string_to_list("""
            <?php
            if (true) {
                if (false) {
                    if (true) {
                        echo "Nevermind.";
                    }
                }
            }
            ?>""")
        self._test(source, expected)

    def test_standard_begin_end_tags(self):
        source = string_to_list("<% echo 'hi'; %>")
        expected = string_to_list("""
            <?php
            echo 'hi';
            ?>""")
        self._test(source, expected)

if __name__ == "__main__":
    unittest.main()