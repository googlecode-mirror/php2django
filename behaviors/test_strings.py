""" Tests for string parsing behaviors. """
import unittest
import strings
from utils import string_to_list

class TestHereDoc(unittest.TestCase):
    # I know this is woefully lacking, but here's a quick example.

    def test_no_here_docs(self):
        php_lines = string_to_list("""
            <?php
            echo "Hello world"
            ?>""")
        updated_php, updated_python = strings.grab_heredocs(php_lines, [])
        self.assertEqual(updated_php, php_lines, "PHP should not have changed.")
        self.assertEqual(len(updated_python), 0, "Should be no python.")

    def test_one_here_docs(self):
        #NOTE: This is pretty nasty to code. I wonder if we can make it easier
        # by allowing behaviors to accept multi-line strings, rather than lists
        # of lines? Or by stripping the \n during file input? Maybe...
        php_lines = string_to_list("""
            <?php
            echo "Hello world";
            x = <<<EOF
            Whatever, dude.
            EOF;
            ?>""")
        expected_php = string_to_list("""
            <?php
            echo "Hello world";
            x = HEREDOC_1
            ?>""")
        expected_python = string_to_list('''
            HEREDOC_1 = """
            Whatever, dude.
            """''')
        updated_php, updated_python = strings.grab_heredocs(php_lines, [])
        self.assertEqual(updated_php, expected_php)
        self.assertEqual(updated_python, expected_python)

if __name__ == "__main__":
    unittest.main()