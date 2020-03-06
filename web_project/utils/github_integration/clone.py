# clone.py
#
# Created By: Sebastian Prado     Sebastian.Prado@CalBaptist.edu
# Last Edited: March 6, 2020
#
# Description:
#       clone.py is a script with a function to clone a github repository and place it in a temporary folder within the application.
#
import sys
import git
import tempfile
import os
from datetime import datetime
from ideal_classroom.models import UserDetail


timeStamp = datetime.now().time()
basePath = os.getcwd()
userName = request.user.username
gitHubID = UserDetail.objects.get(User = userName).values('GitHubUsername')

#Temporary File to store users code
tempfile.tempdir = '/{BasePath}/{Github_id}-{TimeStamp}'.format(BasePath=basePath, Github_id = gitHubID, TimeStamp = timeStamp)
tempFile = tempfile.TemporarFile()

#Generated github link
assignment_link = 'http://github.com/{Github_prefix}/{Github_id}'.format(Github_id=gitHubID)

#Function that will clone GitHub Repository to specified path
#   PRE: gitRepo is the absolute path of where the repository will be cloned to
#   POST: Creates a cloned repository in the tempFolder

def cloneGit(tempFolder, gitRepo):
	git.Git(tempFolder).clone(gitRepo)

cloneGit(tempFile, assignment_link)