"""
Converters convert PHP code to python code by stringing together multiple
behaviors.
"""
from behaviors.comments import comment_unconverted_lines
from behaviors.strings import grab_heredocs

class Converter(object):
    """
    Converts PHP lines into python lines.
    The "convert" function is the workhorse, but its functionality depends on
    multiple behaviors. See behaviors/README.txt for more details.
    """
    def __init__(self, behaviors=[]):
        self.php_lines = []
        self.python_lines = [] #\n terminated!
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
    return Converter([grab_heredocs, comment_unconverted_lines])