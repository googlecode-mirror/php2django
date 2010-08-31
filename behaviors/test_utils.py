import unittest
from utils import string_to_list, side_by_side

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

class TestSideBySide(unittest.TestCase):
    # This is marginally silly, but why not test it anyway?
    def test1(self):
        got = side_by_side(["one", "two",], ["1","2",], 12) #12 for convenience
        expected = "\n".join(['',
            #1234567890123456789012345
            " Side-by-side comparison ",
            "____Got_____|__Expected__",
            "one         |1           ",
            "two         |2           ",])
        self.assertEqual(got, expected)

if __name__ == "__main__":
    unittest.main()