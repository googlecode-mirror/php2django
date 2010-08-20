About Behaviors
===============
Behaviors are simply short code chunks that can be swapped in and out. See the
converters.py file for examples of how to plug them in.

Each function follows this signature: some_behavior(php_lines, python_lines).
Each function returns a tuple of (updated_php_lines, updated_python_lines).
This allows for chaining of behaviors and also for targeted testing.
We could use objects, if they implement __call__(php_lines, python_lines).
