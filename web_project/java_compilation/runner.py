# runner.py
#
# Created By: Alex Peterson     AlexJoseph.Peterson@CalBaptist.edu
# Last Edited: Feb 20, 2020
#
# Description:
#       runner.py is a script used to demonstrate the ability to compile Java classes,
#       and JUnit tests automatically.
#

import os
from compile import compile_java_class
from compile import compile_java_test
from compile import run
from compile import run_tests



# There are two current ways to compile and run a JAVA class and/or a JAVA test class.

# 1) Compile the java class, and java test class seperately, then run.
compile_java_class("Calculator.java")
compile_java_test("CalculatorTest.java")


# 2) compile and run both classes at once.
print(run_tests("Calculator.java", "CalculatorTest.java"))
