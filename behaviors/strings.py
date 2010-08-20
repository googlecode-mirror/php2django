"""
String parsing behaviors.
"""
from php_tokens import *

def grab_heredocs(php_lines, python_lines):
    """
    Grab multi-line strings.
    """
    #TODO:
    # 1. Check for funky escape characters:
    # http://www.php.net/manual/en/language.types.string.php#language.types.string.syntax.heredoc
    # 2. Replace $variable substitutions with python string formatting.
    # 3. Handle statements after the end_heredoc_marker?? (Is that valid in PHP?)
    updated_php_lines = []
    updated_python_lines = python_lines[:] #copy all to start
    block_string = False
    count = 0
    for line in php_lines:
        if block_string:
            if end_heredoc_marker in line:
                block_string = False
                updated_python_lines.append('"""\n')
                continue
            updated_python_lines.append(line)
            continue
        if T_START_HEREDOC in line:
            block_string = True
            before, after = line.split(T_START_HEREDOC)
            end_heredoc_marker = after[:3] + ';'
            count += 1
            next_string = "HEREDOC_%d" % count
            updated_php_lines.append( "%s%s\n" % (before, next_string))
            updated_python_lines.append( '%s = """%s' % (next_string, after[3:]))
            continue
        # otherwise, just pass the line through for further processing
        updated_php_lines.append(line)

    return (updated_php_lines, updated_python_lines)