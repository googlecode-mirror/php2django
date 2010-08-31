"""
Code-prettification functions.
"""

INDENT = " " * 4

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

def _split_php_line(php_line):
    """
    Tries to split a php_line into multiple lines. Returns a list of split
    lines. Some items in this list may not be complete lines, but remainders
    of lines.
    NOTE: This requires:
    - php_line is a (partial) valid PHP line, without any mix-ins of HTML.
    - Hence, php_line contains no "<?=" or "<%=" tags.
    - It may contain up to one PHP-opening tag (at the beginning)
    - It may contain up to one PHP-closing tag (at the end)
    """
    splits  = []
    working = php_line.strip()
    # Detect beginning and ending tags.
    has_beginning_tag = False
    has_ending_tag = False
    for token in ('<?php', '<?', '<%'):
        if working.find(token) == 0:
            working = working.replace(token, '')
            has_beginning_tag = True
            break
    for token in ('?>', '%>'):
        if len(working) > 2 and working[-2:] == token:
            working = working.replace(token, '')
            has_ending_tag = True
            break

    # Split on specific characters:
    done = (len(working) < 1)
    while (not done):
        done = True
        in_quotes = []
        for i in range(0, len(working)):
            char = working[i]
            if char in ("'", '"'):
                if len(in_quotes) > 0 and in_quotes[-1] == char:
                    in_quotes = in_quotes[:-1]
                else:
                    in_quotes.append(char)
            elif char in (';', '{', '}'):
                if len(in_quotes) > 0:
                    continue
                else:
                    splits.append( working[:i+1] )
                    working = working[i+1:]
                    done = (len(working) < 1)
                    break # out of for loop
            elif char in (':', ):
                if len(in_quotes) > 0:
                    continue
                if "case " in working[:i-1]:
                    splits.append( working[:i+1] )
                    working = working[i+1:]
                    done = (len(working) < 1)
                    break # out of for loop

    if len(working) > 0:
        splits.append(working)
    # Strip them all.
    strips = []
    for line in splits:
        stripped = line.strip()
        if len(stripped) > 0:
            strips.append(stripped)
    # Handle beginning and ending tags.
    if has_beginning_tag:
        strips.insert(0, "<?php")
    if has_ending_tag:
        strips.append("?>")
    return strips


def consolidate_php(php_lines, python_lines):
    """Consolidate multi-line php_lines to single-lines.

    Does not affect python_lines at all.
    NOTE: Assumes all php_lines are actually PHP, not embedded HTML.
    """
    pretties = []

    # Split any multi-line statements first.
    splits = []
    for line in php_lines:
        bare = line.strip()
        splits.extend(_split_php_line(bare))

    # Now, try to process single lines (and partial lines):
    level = 0 # indentation level
    remain = "" # remainder from previous line
    for line in splits:
        spaces = INDENT * level
        bare = line.strip()
        if '<?php' in bare:
            pretties.append(bare[:5])
            remain = bare[5:].strip()
            level = 0
            continue
        if bare in ('<?php', '?>'):
            pretties.append(bare)
            level = 0
            continue
        if 'case ' in bare:
            if bare[-1] == ':':
                pretties.append(spaces + remain + bare)
                remain = ""
                level += 1
                continue
        if 'break;' == bare:
            pretties.append(spaces + remain + bare)
            level -= 1
            remain = ""
            continue
        if bare[-1] in (';', ):
            pretties.append(spaces + remain + bare)
            remain = ""
            continue
        if bare[-1] in ('{', ):
            pretties.append(spaces + remain + bare)
            level += 1
            remain = ""
            continue
        if bare[-1] in ('}', ):
            level -= 1
            spaces = INDENT * level
            if level < 0: level = 0
            pretties.append(spaces + remain + bare)
            remain = ""
            continue
        remain = bare + " "
    return (pretties, python_lines)

if __name__ == "__main__":
    print "_split_php_line sanity test."
    print _split_php_line("")
    print _split_php_line("echo 'test';")
    print _split_php_line("echo 'test';echo 'next';")
    print _split_php_line("if (0) { echo 'test';")
    print _split_php_line("if (0) { echo 'test'; }")
    print _split_php_line("switch ($i) { case 0: echo 'blah'; }")
    print _split_php_line(
            '<?php switch ($i) { '
            'case 0: echo "i equals 0"; break; '
            'case 1: echo "i equals 1"; break; '
            'case 2: echo "i equals 2"; break; '
            '} '
            'if (true) { echo "True"; } else { echo "False"; }'
            '?>')