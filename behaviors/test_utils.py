import unittest
from utils import string_to_list

class TestStringToList(unittest.TestCase):
    def test_indented(self):
        source = """
           one
           two
           three"""
        expected = ["one", "two", "three", ]
        got = string_to_list(source)
        self.assertEqual(got, expected)
        
    def test_nonindented(self):
        source = """one\ntwo\nthree"""
        expected = ["one", "two", "three", ]
        got = string_to_list(source)
        self.assertEqual(got, expected)
                
    def test_funky_indented(self):
        source = """
           one
        two
     three"""
        expected = ["           one", "        two", "     three", ]
        got = string_to_list(source)
        self.assertEqual(got, expected)        
