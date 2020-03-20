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

# Get the information of the user (GitHub ID, Name, Assignment, Course)

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


#Pass through information to run tests
#def test_runner(github_id, student_name, assignment, course):
    #clone.cloneGit()   #params need to be fixed. Should not run correctly. 
    
    #pass
