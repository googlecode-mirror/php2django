"""
Converts a PHP module to a python module.
Does super-simple substitutions, rather than fancy parsing.
"""
from converters import get_converter1

def main():
    php_file = open("php_source/HTTPPost.php")
    php_lines = php_file.readlines()
    php_file.close()

    converter = get_converter1()
    converter.convert(php_lines)
    python_file = open("python_out/HTTPPost.py", "w")
    python_file.writelines(converter.python_lines)
    python_file.close()

if __name__ == "__main__":
    main()