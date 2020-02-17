from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from hello.models import Course, HelloTest

def home(request):
    return HttpResponse("Welcome, Django! This is a test to make sure we can update Google Cloud. Worked here!")

# A test page to test if the database integration is working properly - Added by Micah Steinbock on Feb 16, 2020
def dbtest(request):
    # Course = a model that is connected to the GC MySQL DB
    rows = Course.objects.all()
    # rows = HelloTest.objects.all()
    return render(request, "dbtest.html", {"rows" : rows })

# A login page to test HTML templates - Added by Austen Combs on Feb 17, 2020
def login(request):
    #return HttpResponse("As an authorized user, please enter your valid credentials!")
    return render(request, "login.html")