from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

# User home page - Edited by Austen Combs on Feb 17, 2020
def home(request):
    return render(request, "home.html")

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

