from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .models import Course, Roster, Assignment, Submission, AuthUser, UserDetail
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib import messages
from test_runner import test_runner
from datetime import datetime

# User home page - Edited by Austen Combs on Feb 20, 2020
def home(request):
    if request.user.is_authenticated:
        return redirect('account')
    else:
        return redirect('login')
    return render(request, "home.html")

# Login form page - Updated by Abanoub Farag on Feb 23, 2020
def login_view(request):
    setattr(request, 'view', 'login')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('account')
    else:
        form = AuthenticationForm() 
    return render(request, 'login.html', {'form': form})

# Logout page - Created by Micah Steinbock on April 2, 2020
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

# User registration page - Updated by Abanoub Farag on March 27, 2020
def register(request):
    setattr(request, 'view', 'register')
    if request.method == 'POST':
        userInfo = forms.UserCreationForm(request.POST)
        details = forms.Register(request.POST)
        if userInfo.is_valid() and details.is_valid():
            #Save the form data
            infoInstance = userInfo.save(commit=False)
            detailsInstance = details.save(commit=False)
            #Set info in the User table to info gathered in the UserDetail section
            #NOT CURRENTLY ADDING ANYTHING
            infoInstance.email = detailsInstance.Email
            infoInstance.first_name = detailsInstance.Firstname
            infoInstance.last_name = detailsInstance.Lastname
            #Save the User entry
            infoInstance.save()
            #Link the details to that User entry and save it
            detailsInstance.User = infoInstance
            detailsInstance.save()
            login(request, infoInstance)
            return redirect('account')
    else:
        userInfo = forms.UserCreationForm()
        details = forms.Register()
    return render(request, 'register.html', {'userInfo': userInfo, 'details': details})

# User account page - Added by Austen Combs on Feb 17, 2020
@login_required(login_url="login")
def account(request):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'account')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, "account.html", {'userDetails': userDetails,'courses':courses})

@login_required(login_url="login")
def edit_info(request):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'edit')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    if request.method == 'POST':    
        form = forms.EditInfo(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            userDetails.Email = instance.Email
            userDetails.Firstname = instance.Firstname
            userDetails.Lastname = instance.Lastname
            userDetails.SchoolID = instance.SchoolID
            userDetails.GitHubUsername = instance.GitHubUsername
            userDetails.save()
            user = userDetails.User
            user.email = instance.Email
            user.first_name = instance.Firstname
            user.last_name = instance.Lastname
            user.save()
            return redirect('account')
    else:
        form = forms.EditInfo(initial={'Email':userDetails.Email, 'Firstname':userDetails.Firstname, 'Lastname':userDetails.Lastname, 'SchoolID':userDetails.SchoolID, 'GitHubUsername':userDetails.GitHubUsername})

    return render(request, 'edit_info.html', {'userDetails':userDetails,'form':form,'courses':courses})

#Page where an instructor can create a course - Added by Micah Steinbock on March 6, 2020
@login_required(login_url="login")
def create_course(request):
    #Only allow teachers to navigate to this page
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'create_course')
    if not userDetails.isTeacher:
        return redirect('account')

    if request.method == 'POST':
        form = forms.CreateCourse(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.InstructorID = request.user
            instance.save()
            return redirect('account')
    else:
        form = forms.CreateCourse()
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, 'create_course.html', {'form':form,'userDetails':userDetails,'courses':courses})

# Will show a list of all courses that the user is enrolled in - Added by Austen Combs on Feb 20, 2020
#Temp removed by Micah Steinbock on April 3, 2020
@login_required(login_url="login")
def courses(request):
    return redirect('account')
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'courses')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, "course.html", {'courses':courses, 'userDetails':userDetails})

#Page where a student can enroll in a course - Added by Micah Steinbock on March 12, 2020
@login_required(login_url="login")
def enroll(request):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'enroll')
    if request.method == 'POST':
        form = forms.Enroll(request.POST)
        if form.is_valid():
            course_password = form.cleaned_data['course_password']
            num_results = Course.objects.filter(Password=course_password).count()
            #If the course_password is valid (there is an entry with that unique code)
            if num_results == 1:
                course = Course.objects.get(Password=course_password)
                num_results = Roster.objects.filter(UserID=request.user, CourseID=course).count()
                if num_results == 0:
                    instance = Roster()
                    instance.UserID = request.user
                    instance.CourseID = course
                    instance.Classification = "Student"
                    instance.NumExtensions = 3
                    instance.save()
                    return redirect('account')
                else:
                    messages.add_message(request, messages.INFO, 'You have already enrolled in this class')
            else:
                #Alert if the code is not valid
                messages.add_message(request, messages.INFO, 'Invalid Course Enrollment Code')
    else:
        form = forms.Enroll()
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, 'enroll.html', {'form':form,'userDetails':userDetails,'courses':courses})

# user page where the details are displayed for 1 course - Added by Micah Steinbock on March 19, 2020
@login_required(login_url="login")
def course_details(request, course_id):
    course = Course.objects.get(Slug=course_id)
    assignments = Assignment.objects.filter(CourseID = course)
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'course_details')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, 'course_details.html', {'course':course,'assignments':assignments, 'userDetails':userDetails,'courses':courses})

@login_required(login_url="login")
def edit_course(request, course_id):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'edit')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)

    course = Course.objects.get(Slug = course_id)
    if request.method == 'POST':
        form = forms.EditCourse(request.POST)
        if form.is_valid():
            
            instance = form.save(commit=False)
            course.Title = instance.Title
            course.Code = instance.Code
            course.Description = instance.Description
            course.GitHubPrefix = instance.GitHubPrefix
            course.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
    else:
        form = forms.EditCourse(initial={'Title':course.Title, 'Code':course.Code, 'Description':course.Description, 'Slug':course.Slug, 'GitHubPrefix':course.GitHubPrefix})

    return render(request, 'edit_course.html', {'userDetails':userDetails,'courses':courses,'form':form,'course':course})

# Will show a list of all assignments that are in the given course - Added by Austen Combs on Feb 20, 2020
# Temp removed by Micah Steinbock on April 3, 2020
@login_required(login_url="login")
def assignments(request, course_id):
    return redirect('account')
    course = Course.objects.get(Slug=course_id)
    assignments = Assignment.objects.filter(CourseID = course)
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'assignments')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, "assignment.html", {'course':course, 'assignments':assignments, 'userDetails':userDetails,'courses':courses})

# user page where the details are displayed for 1 assignment - Added by Micah Steinbock on March 19, 2020
@login_required(login_url="login")
def assignment_details(request, course_id, assn_name):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'assignment_details')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    if userDetails.isTeacher:
        course = Course.objects.get(Slug=course_id)
        assignment = Assignment.objects.get(Slug=assn_name)
        return render(request, 'assignment_details.html', {'course':course,'assignment':assignment,'userDetails':userDetails,'courses':courses})
    else:
        #Student View
        course = Course.objects.get(Slug=course_id)
        assignment = Assignment.objects.get(Slug= assn_name)
        roster = Roster.objects.get(UserID = request.user, CourseID = course)
        pastSubmission = Submission.objects.filter(AssignmentID = assignment, RosterID = roster)
        if request.method == 'POST':
            #Define parameters
            Username = request.user.username
            GitHubUserName = UserDetail.objects.get(User = request.user).GitHubUsername
            CoursePrefix = course.GitHubPrefix
            AssignmentPrefix = assignment.GitHubPrefix
            SolutionLink = assignment.SolutionLink
            #Call Code which saves the GradeInfo object to the returnVal object
            returnVal = test_runner(Username,GitHubUserName,CoursePrefix,AssignmentPrefix,SolutionLink)
            #Displays the results of the method call on the webpage as a message response
            messages.add_message(request, messages.INFO, returnVal.comments)
            #If there is already a submission, then overwrite it.
            roster = Roster.objects.get(UserID = request.user, CourseID = course)
            submission = Submission.objects.filter(AssignmentID = assignment, RosterID = roster)
            if submission.count() > 0:
                submission.delete()
            #Adds the grade into the database
            instance = Submission()
            instance.AssignmentID = assignment
            instance.RosterID = roster
            instance.SubmittedOn = datetime.now()
            instance.Grade = (returnVal.passedTests / returnVal.totalTests) * assignment.PossiblePts
            instance.Comments = returnVal.comments
            instance.DidUseExtension = True
            instance.save()
        return render(request, 'assignment_details.html', {'course':course,'assignment':assignment,'pastSubmission':pastSubmission,'userDetails':userDetails,'courses':courses})

@login_required(login_url="login")
def edit_assignment(request, course_id, assn_name):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'edit')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)

    course = Course.objects.get(Slug = course_id)
    assignments = Assignment.objects.filter(CourseID = course)
    assignment = Assignment.objects.get(Slug = assn_name)
    if request.method == 'POST':
        form = forms.EditAssn(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            assignment.Title = instance.Title
            assignment.Description = instance.Description
            assignment.DueDate = instance.DueDate
            assignment.ReleaseDate = instance.ReleaseDate
            assignment.PossiblePts = instance.PossiblePts
            assignment.SolutionLink = instance.SolutionLink
            assignment.ShowSolution = instance.ShowSolution
            assignment.ShowSolutionOnDate = instance.ShowSolutionOnDate
            assignment.NumAttempts = instance.NumAttempts
            assignment.GitHubPrefix = instance.GitHubPrefix
            assignment.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
    else:
        form = forms.EditAssn(initial={'Title':assignment.Title, 'Slug':assignment.Slug, 'Description':assignment.Description, 'DueDate':assignment.DueDate,
            'ReleaseDate':assignment.ReleaseDate, 'PossiblePts':assignment.PossiblePts, 'SolutionLink':assignment.SolutionLink, 'ShowSolution':assignment.ShowSolution,
            'ShowSolutionOnDate':assignment.ShowSolutionOnDate, 'NumAttempts':assignment.NumAttempts, 'GitHubPrefix':assignment.GitHubPrefix})

    return render(request, 'edit_assignment.html', {'userDetails':userDetails,'courses':courses,'form':form,'course':course, 'assignments':assignments, 'assignment':assignment})

#Custom class used in assignment_grades() to store the info for each submission
class combinedGradeInfo():
    def __init__(self):
        self.submission = None
        self.userDetail = None

#Shows a list of grades for all students enrolled in the course - Added by Micah Steinbock on March 26, 2020
@login_required(login_url="login")
def assignment_grades(request, course_id, assn_name):
    #Only allow teachers to navigate to this page
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'assignment_grades')
    if not userDetails.isTeacher:
        return redirect('account')
    
    #Get course and assignment info
    course = Course.objects.get(Slug=course_id)
    assignment = Assignment.objects.get(Slug=assn_name)
    #Get all submissions related to this assignment
    submissions = Submission.objects.filter(AssignmentID = assignment)
    #Create a blank list of submission info
    submission_info = []
    #For each submission entry in the database
    for submission in submissions:
        #Get the user detail info
        user = submission.RosterID.UserID
        userDetail = UserDetail.objects.get(User = user)
        #Store the user detail and submission info in a custom object
        info = combinedGradeInfo()
        info.submission = submission
        info.userDetail = userDetail
        #Add that object into the list
        submission_info.append(info)

    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, 'assignment_grades.html', {'course':course, 'assignment':assignment, 'submission_info':submission_info, 'userDetails':userDetails,'courses':courses})

#Creation page for assignments - Added by Micah Steinbock on March 10, 2020
@login_required(login_url="login")
def create_assignment(request, course_id):
    #Only allow teachers to navigate to this page
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'create_assignment')
    if not userDetails.isTeacher:
        return redirect('account')
    
    course = Course.objects.get(Slug=course_id)
    if request.method == 'POST':
        form = forms.CreateAssignment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.CourseID = course
            instance.hasRun = False
            instance.save()
            return redirect('account')
    else:
        form = forms.CreateAssignment()

    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, 'create_assignment.html', {'form':form, 'course':course, 'userDetails':userDetails,'courses':courses})

@login_required(login_url="login")
def grades(request, course_id):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'grades')
    course = Course.objects.get(Slug=course_id)
    roster = Roster.objects.get(UserID = request.user, CourseID = course)
    grades = Submission.objects.filter(RosterID = roster)
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)
    return render(request, 'grades.html', {'course':course, 'grades':grades,'userDetails':userDetails,'courses':courses})

@login_required(login_url="login")
def edit_grades(request, course_id, assn_name, username):
    userDetails = UserDetail.objects.get(User = request.user)
    setattr(request, 'view', 'edit')
    if userDetails.isTeacher:
        courses = Course.objects.filter(InstructorID = request.user)
    else:
        courses = Roster.objects.filter(UserID = request.user)

    course = Course.objects.get(Slug=course_id)
    assignment = Assignment.objects.get(Slug=assn_name)
    currentUser = User.objects.get(username = username)
    roster = Roster.objects.get(CourseID=course, UserID=currentUser)
    submission = Submission.objects.get(AssignmentID=assignment, RosterID=roster)


    if request.method == 'POST':
        form = forms.EditGrades(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            submission.Grade = instance.Grade
            submission.Comments = instance.Comments
            submission.DidUseExtension = instance.DidUseExtension = True
            submission.save()
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
    else:
        form = forms.EditGrades(initial={'Grade':submission.Grade, 'Comments':submission.Comments, 'DidUseExtension':submission.DidUseExtension})

    return render(request, 'edit_grades.html', {'userDetails':userDetails,'courses':courses,'form':form,'course':course, 'assignment':assignment,
    'submission':submission, 'username':username})