"""
Converts a PHP module to a python module.
Does super-simple substitutions, rather than fancy parsing.
"""
from php_tokens import *

class Converter(object):
    def __init__(self):
        self.php_lines = []
        self.python_lines = [] #\n terminated!

    def _grab_heredocs(self):
        """
        Grab multi-line strings and put them up top.
        """
        #TODO:
        # 1. Check for funky escape characters:
        # http://www.php.net/manual/en/language.types.string.php#language.types.string.syntax.heredoc
        # 2. Replace $variable substitutions with python string formatting.
        # 3. Handle statements after the end_heredoc_marker?? (Is that valid in PHP?)
        new_php_lines = []
        block_string = False
        count = 0
        for line in self.php_lines:
            if block_string:
                if end_heredoc_marker in line:
                    block_string = False
                    self.python_lines.append('"""\n')
                    continue
                self.python_lines.append(line)
                continue
            if T_START_HEREDOC in line:
                block_string = True
                before, after = line.split(T_START_HEREDOC)
                end_heredoc_marker = after[:3] + ';'
                count += 1
                next_string = "HEREDOC_%d" % count
                new_php_lines.append( "%s%s\n" % (before, next_string))
                self.python_lines.append( '%s = """%s' % (next_string, after[3:]))
                continue
            # otherwise, just pass the line through for further processing
            new_php_lines.append(line)

        self.php_lines = new_php_lines

    def _comment_unconverted_lines(self):
        """
        Comment-out any remaining PHP lines that were not converted.
        """
        self.python_lines.append("# The following lines were not converted:\n")
        for line in self.php_lines:
            self.python_lines.append("#%s" % line)
        self.php_lines = []

    def convert(self, php_lines):
        """
        Reads a list of php_lines and converts them to python_lines.
        """
        self.php_lines = php_lines
        self._grab_heredocs()
        #self._convert_block_comments()
        #and more...?
        self._comment_unconverted_lines() #save this for last.

def main():
    php_file = open("php_source/HTTPPost.php")
    php_lines = php_file.readlines()
    php_file.close()

    converter = Converter()
    converter.convert(php_lines)
    python_file = open("python_out/HTTPPost.py", "w")
    python_file.writelines(converter.python_lines)
    python_file.close()

if __name__ == "__main__":
    main()