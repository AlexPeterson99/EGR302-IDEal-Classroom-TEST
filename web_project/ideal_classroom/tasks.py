import time, schedule
from datetime import datetime
from .models import Assignment
from test_runner import test_print

def check_time():
    # the amount of grace to give in hours
    grace_period = 1
    # pull dates from database and fill in instead of hardcoded value
    assignments = Assignment.objects.filter(hasRun = False)
    for a in assignments:
        d = a.DueDate
        check = datetime(d.year, d.month, d.day, d.hour + grace_period, d.minute)
        now = datetime.now()
        if (compare_to(check, now) <= 0):
            run_tests(a)


def run_tests(a):
    # make sure assignment only runs once
    a.hasRun = True
    # get a list of all the students in the course
    roster_entries = Roster.objects.filter(CourseID = a.CourseID)
    for row in roster_entries:
        # get user information
        curr_user = row.UserID
        username = curr_user.username
        github_username = UserDetail.objects.get(User = curr_user).GitHubUsername
        course_prefix = a.CourseID.GitHubPrefix
        assignment_prefix = a.GitHubPrefix
        solution = a.SolutionLink
        # run tests and save return value
        return_val = test_print(username, github_username, course_prefix, assignment_prefix, solution)
        submission = Submission.objects.filter(AssignmentID = a, RosterID = row)
        # if a submission already exists delete it
        if submission.count() > 0:
            submission.delete()
        # generate new submission
        instance = Submission()
        instance.AssignmentID = a
        instance.RosterID = row
        instance.SubmittedOn = datetime.now()
        instance.Grade = (return_val.passedTests / return_val.totalTests) * a.PossiblePts
        instance.Comments = return_val.comments
        instance.DidUseExtension = False
        instance.save()


def compare_to(date, other):
    if (date.year != other.year):
        return date.year - other.year
    elif (date.month != other.month):
        return date.month - other.month
    elif (date.day != other.day):
        return date.day - other.day
    elif (date.hour != other.hour):
        return date.hour - other.hour
    elif (date.minute != other.minute):
        return date.minute - other.minute
    else:
        return date.second - other.second
    


schedule.every(3).hours.do(check_time)

while True:
    schedule.run_pending()
    time.sleep(1)