"""
Utility functions for making hacking PHP from python easier.
"""

def string_to_list(source_string):
    """
    This is mainly to allow more readable multi-line code blocks in tests.
    Converts a valid source_string to a list by:
      1. splitting on newlines
      2. figuring out the indentation from the first line.
      3. removing that indentation from every line.
    Valid source strings:
      A. must begin with an empty line, like this:
        src = '''
            test
            of
            multiple
            lines'''
      B. must not contain any tab characters for white-space at the beginning
    Invalid source strings are simply split and returned as-is.
    """
    valid = True # assume the best
    temp = source_string.split("\n")
    if len(temp[0]) > 0:
        return temp
    x = 0
    while temp[1][x] == ' ':
        x += 1
    fixed = []
    for line in temp[1:]:
        if line[:(x-1)] == ' '*(x-1):
            fixed.append(line[x:])
        else:
            valid = False
            break
    if valid:
        return fixed
    else:
        return temp[1:]

def side_by_side(left, right, chars_per_column=40):
    """
    Formats left and right lists side-by-side.
    """
    if len(left) > len(right):
        for i in range(0, len(left) - len(right)):
            right.append("")
    else:
        for i in range(0, len(right) - len(left)):
            left.append("")
    msg = [
        '',
        "Side-by-side comparison".center(2*chars_per_column + 1),
        ("Got".center(chars_per_column,"_") +
         "|" +
         "Expected".center(chars_per_column,"_")
        ),
    ]
    for l, r in zip(left, right):
        msg.append("%s|%s" % (l.ljust(chars_per_column), r.ljust(chars_per_column)))
    return "\n".join(msg)
