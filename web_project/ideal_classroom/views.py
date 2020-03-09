from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .models import Course, Assignment, Submission, AuthUser, UserDetail
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms

# User home page - Edited by Austen Combs on Feb 20, 2020
def home(request):
    users = AuthUser.objects.all()
    courses = Course.objects.all()
    submits = Submission.objects.all()
    return render(request, "home.html", {'users': users, 'courses': courses, 'submits': submits})

# A test page to test if the database integration is working properly - Added by Micah Steinbock on Feb 16, 2020
def dbtest(request):
    # Course = a model that is connected to the GC MySQL DB
    #rows = Course.objects.all()
    # rows = HelloTest.objects.all()
    #return render(request, "dbtest.html", {"rows" : rows })
    return render(request, "dbtest.html")

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
    return render(request, "account.html")

# User course page - Added by Austen Combs on Feb 20, 2020
def course(request):
    courses = Course.objects.all()
    assignments = Assignment.objects.all()
    return render(request, "course.html", {'courses':courses, 'assignments': assignments})

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

def create_assignment(request):
    if request.method == 'POST':
        form = forms.CreateAssignment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('assignment')
    else:
        form = forms.CreateAssignment()
    return render(request, 'create_assignment.html', {'form':form})