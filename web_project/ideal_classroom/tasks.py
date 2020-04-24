from datetime import datetime, timedelta, timezone
from .models import Assignment, Roster, UserDetail, Submission
from test_runner import test_runner
from apscheduler.schedulers.background import BackgroundScheduler

# starts scheduled tasks
def start_tasks():
    print("started")
    #sched = BackgroundScheduler()
    #sched.print_jobs()
    #sched.start()
    #sched.add_job(check_time, 'interval', hours=3, replace_existing=True)


def check_time():
    print("Checked assignments")
    # pull dates from database and fill in instead of hardcoded value
    assignments = Assignment.objects.filter(hasRun = False)
    for a in assignments:
        d = a.DueDate
        check = d - timedelta(hours=6)
        now = datetime.now()
        if (compare_to(check, now) <= 0):
            run_tests(a)


def run_tests(a):
    # make sure assignment only runs once
    a.hasRun = True
    a.save()
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
        return_val = test_runner(username, github_username, course_prefix, assignment_prefix, solution)
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