from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .models import Course, Roster, Assignment, Submission, AuthUser, UserDetail
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms
from django.contrib import messages
from test_runner import test_print

# User home page - Edited by Austen Combs on Feb 20, 2020
def home(request):
    return render(request, "home.html")

# Login form page - Updated by Abanoub Farag on Feb 23, 2020
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            return redirect('account')
    else:
        form = AuthenticationForm() 
    return render(request, 'login.html', {'form': form})

# User registration page - Updated by Abanoub Farag on Feb 23, 2020
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log the user in
            return redirect('account')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User account page - Added by Austen Combs on Feb 17, 2020
def account(request):
    users = AuthUser.objects.all()
    courses = Course.objects.all()
    submits = Submission.objects.all()
    return render(request, "account.html", {'users': users, 'courses': courses, 'submits': submits})

#Page where an instructor can create a course - Added by Micah Steinbock on March 6, 2020
def create_course(request):
    if request.method == 'POST':
        form = forms.CreateCourse(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.InstructorID = request.user
            instance.save()
            return redirect('courses')
    else:
        form = forms.CreateCourse()
    return render(request, 'create_course.html', {'form':form})

# Will show a list of all courses that the user is enrolled in - Added by Austen Combs on Feb 20, 2020
def courses(request):
    enrolled_courses = Roster.objects.filter(UserID = request.user)
    return render(request, "course.html", {'enrolled_courses':enrolled_courses})

#Page where a student can enroll in a course - Added by Micah Steinbock on March 12, 2020
def enroll(request):
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
                    return redirect('courses')
                else:
                    messages.add_message(request, messages.INFO, 'You have already enrolled in this class')
            else:
                #Alert if the code is not valid
                messages.add_message(request, messages.INFO, 'Invalid Course Enrollment Code')
    else:
        form = forms.Enroll()
    return render(request, 'enroll.html', {'form':form})

# user page where the details are displayed for 1 course - Added by Micah Steinbock on March 19, 2020
def course_details(request, course_id):
    course = Course.objects.get(Slug=course_id)
    assignments = Assignment.objects.filter(CourseID = course)
    return render(request, 'course_details.html', {'course':course, 'assignments':assignments})

# Will show a list of all assignments that are in the given course - Added by Austen Combs on Feb 20, 2020
def assignments(request, course_id):
    course = Course.objects.get(Slug=course_id)
    assignments = Assignment.objects.filter(CourseID = course)
    return render(request, "assignment.html", {'course':course, 'assignments':assignments})

# user page where the details are displayed for 1 assignment - Added by Micah Steinbock on March 19, 2020
def assignment_details(request, course_id, assn_name):
    course = Course.objects.get(Slug=course_id)
    assignment = Assignment.objects.get(Slug= assn_name)

    if request.method == 'POST':
        #Define parameters
        Username = request.user.username
        GitHubUserName = UserDetail.objects.get(User = request.user).GitHubUsername
        CoursePrefix = course.GitHubPrefix
        AssignmentPrefix = assignment.GitHubPrefix
        #Call Code
        returnVal = test_print(Username,GitHubUserName,CoursePrefix,AssignmentPrefix)
        messages.add_message(request, messages.INFO, returnVal)
    
    return render(request, 'assignment_details.html', {'course':course,'assignment':assignment})

#Creation page for assignments - Added by Micah Steinbock on March 10, 2020
def create_assignment(request, course_id):
    course = Course.objects.get(Slug=course_id)
    if request.method == 'POST':
        form = forms.CreateAssignment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.CourseID = course
            instance.save()
            return redirect('assignments')
    else:
        form = forms.CreateAssignment()
    return render(request, 'create_assignment.html', {'form':form, 'course':course})