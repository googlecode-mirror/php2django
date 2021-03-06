"""
Converters convert PHP code to python code by stringing together multiple
behaviors.
"""
from behaviors.comments import comment_unconverted_lines, standardize_comments
from behaviors.strings import grab_heredocs
from behaviors.pretty import strip_php_newlines, add_python_newlines
from behaviors.pretty import consolidate_php

class Converter(object):
    """
    Converts PHP lines into python lines.
    The "convert" function is the workhorse, but its functionality depends on
    multiple behaviors. See behaviors/README.txt for more details.
    """
    def __init__(self, behaviors=[]):
        self.php_lines = []
        self.python_lines = []
        self.behaviors = behaviors

    def convert(self, php_lines):
        """
        Reads a list of php_lines and converts them to python_lines.
        """
        self.php_lines = php_lines
        print "Start conversion."
        for behavior in self.behaviors:
            comment = behavior.__doc__.strip()
            if '\n' in comment:
                comment = behavior.__doc__.split('\n')[0]
            print "- %s : %s" % (behavior.__name__, comment)
            (self.php_lines, self.python_lines) = behavior(self.php_lines, self.python_lines)
        print "Finish conversion."

# These functions make it super easy to swap-out functionality, but still
# keep track of what combinations worked in the past.
def get_converter1():
    return Converter([
        strip_php_newlines,
        grab_heredocs,
        comment_unconverted_lines,
        add_python_newlines,
        ])

# Add PHP-pretty functions in.
#NOTE: These don't work quite yet, because of the comment behavior issues.
def get_converter2():
    return Converter([
        strip_php_newlines,
        grab_heredocs,
        standardize_comments,
        consolidate_php,
        comment_unconverted_lines,
        add_python_newlines,
        ])