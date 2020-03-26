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
#import compile
#import clone


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
def test_print(username, github_id, course_prefix, assignment_prefix):
    assignment_link = 'https://github.com/{CoursePrefix}/{AssignmentPrefix}-{GitHubId}'.format(GitHubId=github_id,CoursePrefix=course_prefix,AssignmentPrefix=assignment_prefix)
    print(assignment_link)
    print(username)
    #Creates a new GradeInfo object and fills in the necessary info
    returnVal = GradeInfo()
    returnVal.passedTests = 2   #Temp Test Data
    returnVal.totalTests = 10   #Temp Test Data
    returnVal.comments = username + ', ' + assignment_link  #Temp Test Data
    #Returns the GradeInfo object
    return returnVal

#Pass through information to run tests
#def test_runner(github_id, student_name, assignment, course):
    #clone.cloneGit()   #params need to be fixed. Should not run correctly. 
    
    #pass
