from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from .models import TempUsers
from .models import Course
from .models import Assignment
from .models import Submission

# User home page - Edited by Austen Combs on Feb 20, 2020
def home(request):
    users = TempUsers.objects.all()
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

# User login page - Added by Austen Combs on Feb 17, 2020
def login(request):
    return render(request, "login.html")

# User registration page - Added by Austen Combs on Feb 17, 2020
def register(request):
    return render(request, "register.html")

# User account page - Added by Austen Combs on Feb 17, 2020
def account(request):
    return render(request, "account.html")

# User course page - Added by Austen Combs on Feb 20, 2020
def course(request):
    courses = Course.objects.all()
    assignments = Assignment.objects.all()
    return render(request, "course.html", {'courses':courses, 'assignments': assignments})

# User assignments page - Added by Austen Combs on Feb 20, 2020
def assignment(request):
    assignments = Assignment.objects.all()
    return render(request, "assignment.html", {'assignments': assignments})