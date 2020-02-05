from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django! From Alex! TRUMP 2020!")