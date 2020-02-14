from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome, Django! This is a test to make sure we can update Google Cloud. Worked here!s")