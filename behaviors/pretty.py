"""
Code-prettification functions.
"""

def strip_php_newlines(php_lines, python_lines):
    """Remove newlines from the end of each line in php_lines.
    
    After loading using file.readlines() usually.
    """
    new_php = []
    for line in php_lines:
       if line[-1:] == '\n':
           new_php.append( line[:-1] )
       else:
           new_php.append( line )
    return (new_php, python_lines)
    
def add_python_newlines(php_lines, python_lines):
    """Add newlines to the end of each line in python_lines.
    
    Usually in preparation for saving using file.writelines().
    """
    new_python = [x + '\n' for x in python_lines]
    return (php_lines, new_python)
    

def consolidate_php(php_lines, python_lines):
    """Consolidate multi-line php_lines to single-lines.
    
    Does not affect python_lines at all.
    NOTE: Assumes all php_lines are actually PHP, not embedded HTML.
    """
    pretty = []
    
    
    return (pretty, python_lines)
    
