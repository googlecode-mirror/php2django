import unittest
import pretty
from utils import string_to_list

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

class TestConsolidatePhp(unittest.TestCase):
    def test_semicolon_ending(self):
        pass
        
    def test_open_paren_ending(self):
        pass
        
    def test_close_paren_ending(self):
        pass
        
    def test_switch_statement(self):
        pass

