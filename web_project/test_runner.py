# test_runner.py
#
# Created By: Alex Peterson     AlexJoseph.Peterson@CalBaptist.edu
# Last Edited: March 19, 2020
#
# Description:
#       test_runner.py manages processes involved when a student selects to test their code.
#       Uses utils directory to handle cloning and testing processes.
#
# Dependencies:
# 

#imports
import os
from datetime import datetime
import git
from git import Repo
import tempfile
import contextlib
import shutil, stat
import time
import subprocess
#from utils.java_compilation import compile
#The absolute path of where junit is located.
#Junit us a dependency for compiling JUnit test classes
JUNIT_HOME = "D:\\CBU\\SP20\\EGR302\\Hello-World\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\junit-4.13.jar"
#JUNIT_HOME = "C:\\Users\\bigmo\\OneDrive\\Desktop\\IDEal-Classroom\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\junit-4.13.jar"

#The absolute path of where hamcrest is located.
#hamcrest is a dependency for compiling Junit.
HAMCREST_HOME = "D:\\CBU\\SP20\\EGR302\\Hello-World\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\hamcrest-core-1.3.jar"
#HAMCREST_HOME = "C:\\Users\\bigmo\\OneDrive\\Desktop\\IDEal-Classroom\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\hamcrest-core-1.3.jar"



# GradeInfo created by Micah Steinbock on March 26, 2020
# A custom class object that holds various data that we want to return
# Data:
#   passedTests: an integer number that represents the number of tests the code passed
#   totalTests: an integer number that represents the number of tests that the code was run against
#   comments: a string that contains any information that we want to display to the webpage
class GradeInfo:
    def __init__(self):
        self.passedTests = 0
        self.totalTests = 0
        self.comments = ""


# test_print created by Micah Steinbock on March 19, 2020
# Run when the button on the "assignments_details" page is pressed
# Parameters:
#   username = the IDEal-Classroom username of the currently logged in user
#   github_id = the github username of the currently logged in user
#   course_prefix = the slug for the github classroom prefix
#   assignment_prefix = the slug for the assignment code
#def test_print(username, github_id, course_prefix, assignment_prefix, solution_link):
    #assignment_link = 'https://github.com/{CoursePrefix}/{AssignmentPrefix}-{GitHubId}'.format(GitHubId=github_id,CoursePrefix=course_prefix,AssignmentPrefix=assignment_prefix)
    #print(solution_link)
    #print(assignment_link)
    #print(username)
    #Creates a new GradeInfo object and fills in the necessary info
    #returnVal = GradeInfo()
    #returnVal.passedTests = 3   #Temp Test Data
    #returnVal.totalTests = 10   #Temp Test Data
    #returnVal.comments = username + ', ' + assignment_link  #Temp Test Data
    #Returns the GradeInfo object
    #return returnVal

def test_runner(username, github_id, course_prefix, assignment_prefix, solution_link):
    returnInfo = GradeInfo()
    #Temporary File to store users code
    cwd = os.getcwd()
    with make_temp_directory() as temp_dir:
        assignment_link = 'https://github.com/{CoursePrefix}/{AssignmentPrefix}-{GitHubId}'.format(GitHubId=github_id,CoursePrefix=course_prefix,AssignmentPrefix=assignment_prefix)
        solution_dir = '\\solution\{course}\{assignment}'.format(course=course_prefix, assignment=assignment_prefix)

        # clone calling student's repo
        Repo.clone_from(assignment_link, temp_dir)

        # ***IF CALLING USER DOES NOT HAVE GITHUB PERMISSIONS, THIS SECTION OF CODE WILL FAIL***
        try:
            Repo.clone_from(solution_link, os.getcwd() + solution_dir)
        except:
            g = git.cmd.Git(os.getcwd() + solution_dir)
            g.pull()
        
        src_files = get_src_files(temp_dir)
        tst_file = get_tst_file(solution_dir)

        shutil.copy(tst_file, temp_dir + '\\src')
        cwd = os.getcwd()
        os.chdir(temp_dir + '\\src')
        print(os.getcwd())
        test_name = os.path.split(tst_file)[-1].strip('.java')
        subprocess.run('javac -cp D:\\CBU\\SP20\\EGR302\\Hello-World\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\junit-4.13.jar; *.java')
        #subprocess.run('java -cp .;C:\\Users\\bigmo\\OneDrive\\Desktop\\IDEal-Classroom\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\junit-4.13.jar;C:\\Users\\bigmo\\OneDrive\\Desktop\\IDEal-Classroom\\IDEal-Classroom\\web_project\\utils\\java_compilation\\java_dependencies\\hamcrest-core-1.3.jar org.junit.runner.JUnitCore AssassinManagerInstructorTest')

        with open('result.txt', 'w') as output:
            subprocess.run('java -cp .;{};{} org.junit.runner.JUnitCore {}'.format(JUNIT_HOME, HAMCREST_HOME, test_name), stdout=output)
        with open('result.txt', 'r') as input:
            test_result = input.readlines()
        if("OK" in test_result[-2]):
            num_tests = (test_result[-2].split(' '))[1][1:]
            returnInfo.comments = "All tests passed. (" + num_tests + " out of " + num_tests + ")"
            returnInfo.passedTests = int(num_tests)
            returnInfo.totalTests = int(num_tests)
            print(returnInfo.comments)
        # When there are failing tests
        else:
            print('Tests failed')
            #print(test_result)
            comment = str((' '.join(test_result[get_comments(test_result, '.E'): -1])))
            fail_string = test_result[-2].split(', ')
            nums = []
            for string in fail_string:
                nums.append( (int(string.split(' ')[2])))
            tests_total = nums[0]
            tests_passed = int(nums[0]) - int(nums[1])
            print(tests_passed)
            print(tests_total)
            print(tests_passed/tests_total)
            returnInfo.comments = comment
            returnInfo.passedTests = int(tests_passed)
            returnInfo.totalTests = int(tests_total)
            print(comment)
        os.chdir(cwd)
        #time.sleep(100)
        #compile.compile(temp_dir, solution_dir)


    return returnInfo
    #now?
# Helper: handles temp dir creation and clean up
@contextlib.contextmanager
def make_temp_directory():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, onerror = on_rm_error)

# Helper: handles permission errors when deleting files files from a temp location
def on_rm_error( func, path, exc_info):
    os.chmod( path, stat.S_IWRITE )
    os.unlink( path)

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
        source_files = [ temp_dir + '\\src\\' + fn for fn in os.listdir('src') if fn[-5:] == '.java']
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
def get_tst_file(tst_location):
    path = tst_location + '\\tst\\'
    try:
        tst_file = [file for file in os.listdir(path) if file.endswith('.java')]
        # creates an absolute path
        print(os.getcwd() + path + tst_file[0])
        return os.getcwd() + path + tst_file[0]
    except FileNotFoundError:
        pass


def get_comments(rslt_list, substring):
    for i, s in enumerate(rslt_list):
        if substring in s:
            return i + 2
    return -1


#test_runner("Alex", "AlexPeterson99", "cbu-egr221-sp19", "hw3", "https://github.com/mikiehan/EGR227-HW3-Assassin-Solution")
