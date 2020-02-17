from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from hello.models import Course

def home(request):
    return HttpResponse("Welcome, Django! This is a test to make sure we can update Google Cloud. Worked here!")

def dbtest(request):
    #return render(request, 'dbtest.html')
    rows = Course.objects.all()
    return render(request, "dbtest.html", {"rows" : rows })