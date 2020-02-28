from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log the user in
            return redirect('ideal_classroom.home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            return redirect('ideal_classroom.home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login', {'form': form})