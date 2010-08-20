""" Tests for string parsing behaviors. """
import unittest
import strings

class TestHereDoc(unittest.TestCase):
    # I know this is woefully lacking, but here's a quick example.

    def test_no_here_docs(self):
        php_lines = ['<?php\n', 'echo "Hello world"\n', '?>\n']
        updated_php, updated_python = strings.grab_heredocs(php_lines, [])
        self.assertEqual(updated_php, php_lines, "PHP should not have changed.")
        self.assertEqual(len(updated_python), 0, "Should be no python.")

    def test_one_here_docs(self):
        #NOTE: This is pretty nasty to code. I wonder if we can make it easier
        # by allowing behaviors to accept multi-line strings, rather than lists
        # of lines? Or by stripping the \n during file input? Maybe...
        php_lines = [
            "<?php\n",
            'echo "Hello world";\n',
            'x = <<<EOF\n',
            'Whatever, dude.\n',
            'EOF;\n',
            '?>\n']
        expected_php = [
            '<?php\n',
            'echo "Hello world";\n',
            'x = HEREDOC_1\n',
            '?>\n']
        expected_python = [
            'HEREDOC_1 = ""' + '"\n',
            'Whatever, dude.\n',
            '""' + '"\n']
        updated_php, updated_python = strings.grab_heredocs(php_lines, [])
        self.assertEqual(updated_php, expected_php)
        self.assertEqual(updated_python, expected_python)

