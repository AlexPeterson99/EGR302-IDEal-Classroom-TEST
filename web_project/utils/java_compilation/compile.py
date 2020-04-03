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
from pathlib import Path
import time

#The absolute path of where junit is located.
#Junit us a dependency for compiling JUnit test classes
JUNIT_HOME = "D:\\CBU\\SP20\\EGR302\\Hello-World\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\junit-4.13.jar"
#The absolute path of where hamcrest is located.
#hamcrest is a dependency for compiling Junit.
HAMCREST_HOME = "D:\\CBU\\SP20\\EGR302\\Hello-World\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\hamcrest-core-1.3.jar"

#The time to allow a test to run before declaring a fail result.
#This is handy if the JAVA class being tested has an infinite loop or buggy code.
TEST_TIMEOUT = 10




#The time to allow a test to run before declaring a fail result.
#This is handy if the JAVA class being tested has an infinite loop or buggy code.
TEST_TIMEOUT = 10


# This method retrieves all .java source files found in a given directory
#
#   pre:
#       - temp_dir is the temp path of the repository to be tested.
#       - default cwd when called: C:\Users\Alex\Desktop\IDEalClassroom\IDEal-Classroom\web_project
#   post:
#       - raises FileNotFoundError if temp_dir is not valid.
#       - returns a list of source files.
def get_src_files(temp_dir):
    cwd = os.getcwd()
    os.chdir(temp_dir)
    try:
        source_files = [ fn for fn in os.listdir('src') if fn[-5:] == '.java']
        print('src: ' + source_files[0])
        return source_files
    except FileNotFoundError:
        pass
    finally:
        os.chdir(cwd)


# This method retrieves ***ONE*** .java tst files found in the instructor repository
#
#   pre:
#       - tst_location is the path of the instructor repository.
#   post:
#       - raises FileNotFoundError if tst_location is not valid.
#       - returns a list of tst files.
def get_tst_file(cwd, tst_location):
    direct = os.getcwd()
    os.chdir(cwd)
    path = tst_location + '\\tst\\'
    try:
        tst_file = [file for file in os.listdir(path) if file.endswith('.java')]
        # creates an absolute path
        print(os.getcwd() + path + tst_file[0])
        return os.getcwd() + path + tst_file[0]
    except FileNotFoundError:
        pass
    finally:
        os.chdir(direct)

def compile(temp_dir, solution_dir):
    try:
        cwd = os.getcwd()
        os.chdir(temp_dir + '\src\\')
        src_files = get_src_files(temp_dir)
        tst_file = get_tst_file(cwd, solution_dir)
        #print('tst: ' + tst_file)
        #os.chdir(cwd)
        print(os.getcwd())
        subprocess.run('javac -cp {file}'.format(file= src_files[0]))
        
        #print('we got here. It might have compiled :)')

    except subprocess.TimeoutExpired:
        pass
    except FileNotFoundError:
        pass
    finally:
        print(os.getcwd())
        os.chdir(cwd)

#   Determins if ALL tests passed, or if there are failing tests.
#   pre:
#       - results is a string containing the report from the tests ran.
#   return:
#       - returns true if ALL tests passed.
def is_passing(results):
    return 'OK' in results.splitlines()[:-1 : 2][2]

class CompilationError(Exception):
    pass