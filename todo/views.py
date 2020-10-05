from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
# For creating a new user
from django.contrib.auth.models import User
# for IntegrityError
from django.db import IntegrityError

from django.contrib.auth import login, logout

def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        # create new User.Built in django object to help us makes it really easy to make user object.
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                # redirect user after login
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': 'That username has already been taken. Please choose another username'})
        else:
            # Tell user the password didnt match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')
