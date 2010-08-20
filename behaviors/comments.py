"""
Comment parsing behaviors.
"""
from php_tokens import *

def comment_unconverted_lines(php_lines, python_lines):
    """ Comment-out any remaining PHP lines that were not converted. """
    updated_python_lines = python_lines[:] #copy all
    updated_python_lines.append("# The following lines were not converted:\n")
    for line in php_lines:
        updated_python_lines.append("#%s" % line)
    updated_php_lines = []

    return (updated_php_lines, updated_python_lines)

