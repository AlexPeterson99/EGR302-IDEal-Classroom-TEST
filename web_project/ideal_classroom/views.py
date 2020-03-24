from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .models import Course, Roster, Assignment, Submission, AuthUser, UserDetail
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms
from django.contrib import messages

# User home page - Edited by Austen Combs on Feb 20, 2020
def home(request):
    return render(request, "home.html")

# Login form page - Updated by Abanoub Farag on Feb 23, 2020
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            return redirect('account.html')
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
            return redirect('account.html')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User account page - Added by Austen Combs on Feb 17, 2020
def account(request):
    users = AuthUser.objects.all()
    courses = Course.objects.all()
    submits = Submission.objects.all()
    return render(request, "account.html", {'users': users, 'courses': courses, 'submits': submits})

# User course page - Added by Austen Combs on Feb 20, 2020
def course(request):
    courses = Course.objects.filter(UserID=request.user)
    assignments = Assignment.objects.all()
    return render(request, "course.html", {'courses':courses, 'assignments': assignments})


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
                    return redirect('course')
                else:
                    messages.add_message(request, messages.INFO, 'You have already enrolled in this class')
            else:
                #Alert if the code is not valid
                messages.add_message(request, messages.INFO, 'Invalid Course Enrollment Code')
    else:
        form = forms.Enroll()
    return render(request, 'enroll.html', {'form':form})

#Page where an instructor can create a course - Added by Micah Steinbock on March 6, 2020
def create_course(request):
    if request.method == 'POST':
        form = forms.CreateCourse(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.InstructorID = request.user
            instance.save()
            return redirect('course')
    else:
        form = forms.CreateCourse()
    return render(request, 'create_course.html', {'form':form})

# User assignments page - Added by Austen Combs on Feb 20, 2020
def assignment(request):
    assignments = Assignment.objects.all()
    return render(request, "assignment.html", {'assignments': assignments})

#Creation page for assignments - Added by Micah Steinbock on March 10, 2020
def create_assignment(request, course_id):
    course = Course.objects.get(Slug=course_id)
    if request.method == 'POST':
        form = forms.CreateAssignment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.CourseID = course
            instance.save()
            return redirect('assignment')
    else:
        form = forms.CreateAssignment()
    return render(request, 'create_assignment.html', {'form':form, 'course':course})