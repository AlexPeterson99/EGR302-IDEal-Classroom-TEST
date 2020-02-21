# compile.py
#
# Created By: Alex Peterson     AlexJoseph.Peterson@CalBaptist.edu
# Last Edited: Feb 21, 2020
#
# Description:
#       compile.py is a script with functions to compile, and run JAVA classes and
#       similar JUnit test classes.
#
# Dependencies:
#       - "C:/Users/Alex/Desktop/java_compilation/java_dependencies/junit-4.13.jar"
#       - "C:/Users/Alex/Desktop/java_compilation/java_dependencies/hamcrest-core-1.3.jar"
#
#
# 

import os
import subprocess

#The absolute path of where junit is located.
#Junit us a dependency for compiling JUnit test classes
JUNIT_HOME = "java_dependencies\junit-4.13.jar"
#The absolute path of where hamcrest is located.
#hamcrest is a dependency for compiling Junit.
HAMCREST_HOME = "java_dependencies\hamcrest-core-1.3.jar"

#The time to allow a test to run before declaring a fail result.
#This is handy if the JAVA class being tested has an infinite loop or buggy code.
TEST_TIMEOUT = 10




# This method compiles a single java class.
# Compiling .java file creates a .class file for the same file.
# The .class file is the compiled result.
#
# Uses subprocess to execute command line processes.
#
#   pre:
#       - source_file is the absolute path location of the JAVA class to compile.
#   post:
#       - creates a .class file of source_file.
#       - raises compilationError if compiling source_file is unsuccessful.
#
def compile_java_class(source_file):
    result = subprocess.run(f'javac {source_file}')
    if result.returncode != 0:
        raise CompilationError


# This method compiles a single java test class.
# Compiling .java file creates a .class file for the same file.
# The .class file is the compiled result.
#
# Uses subprocess to execute command line processes.
#
#   pre:
#       - test_file is the absolute path location of the JAVA class to compile.
#       - requires JUnit and Hamcrest dependencies.
#   post:
#       - creates a .class file of test_file.
#       - raises compilationError if compiling source_file is unsuccessful.
#
def compile_java_test(test_file):
    result = subprocess.run(f'javac -cp .;{JUNIT_HOME};{HAMCREST_HOME} {test_file}')
    if result.returncode != 0:
        raise CompilationError


# This method runs a single java class.
# Uses subprocess to execute command line processes.
# Runs JUnit test class, and outputs test results to the command line interface.
#
#   pre:
#       - junit_class is the absolute path location of the test class to run.
#       - requires JUnit and Hamcrest dependencies.
#   post:
#       - outputs test results to the command line interface.
#       - saves a copy of the output results to a text file, for later data analysis.
#       - throws exception if the tests take longer than the allowed time to complete.(in case of poor java implementation)
#   returns:
#       - test result output.
def run(junit_class):
    output = "out.txt"
    with open(output, 'w') as stdout_file:
        try:
            result = subprocess.run(f'java -cp .;{JUNIT_HOME};{HAMCREST_HOME} org.junit.runner.JUnitCore {junit_class}', stdout=stdout_file, timeout=TEST_TIMEOUT)
        except subprocess.TimeoutExpired:
            return 'TEST TIMED OUT'
    with open(output) as f:
        return f.read()


# Compiles and runs java class and associated test at once.
#   pre:
#       - source_file is the java class file.
#       - test_file is the test class file.
#   post:
#       - returns response based on test ressult success.
#
def run_tests(source_file, test_file):
    compile_java_class(source_file)
    compile_java_test(test_file)
    results = run(test_file[0:-5])
    return 'Good job! No Tests Failed.' if is_passing(results) else 'You done oofed!\n\n' + results


#   Determins if ALL tests passed, or if there are failing tests.
#   pre:
#       - results is a string containing the report from the tests ran.
#   return:
#       - returns true if ALL tests passed.
def is_passing(results):
    return 'OK' in results.splitlines()[:-1 : 2][2]