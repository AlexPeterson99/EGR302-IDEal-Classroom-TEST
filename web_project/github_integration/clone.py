# clone.py
#
# Created By: Sebastian Prado     Sebastian.Prado@CalBaptist.edu
# Last Edited: Feb 21, 2020
#
# Description:
#       clone.py is a script with a function to clone a github repository and place it in a generic folder path (FOR NOW).
#
import sys
import git
import tempfile
#from ideal_classroom.models import Course
#from ideal_classroom.models import Assignment

#assignment_link = 'http://github.com/{Github_prefix}/{Assignment}-{Github_id}'.format(Course = course, Semester=semester, Assignment=assignment)

print ("Current temp directory:", tempfile.gettempdir())

tempfile.tempdir = "/TempAssignments"

print ("New temp directory:", tempfile.gettempdir())


#Path that will stored the cloned repository
#TODO: Change path directory to a path within the Application thats more generic

#CLONED_LOCATION = "D:/Test"
#course = Course.objects.filter()

#Function that will clone GitHub Repository to specified path
#sys.argv[1] takes in string that user puts in
#   PRE: CLONED_LOCATION is the absolute path of where the repository will be cloned to
#   POST: Creates a cloned repository in the specified folder
#TODO: Send error when invalid github link is inputted


#git.Git(CLONED_LOCATION).clone(sys.argv[1])

#Output Message that allows user to know that cloning was successful


#output = "Successful!"
#print (output)