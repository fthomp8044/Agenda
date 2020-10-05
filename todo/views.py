from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# For creating a new user
from django.contrib.auth.models import User
# for IntegrityError
from django.db import IntegrityError

from django.contrib.auth import login, logout, authenticate

from .forms import TodoForm

from .models import Todo

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

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        # import authenticate from django auth for built in method for login
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # if password or user doesnt exit
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            # if there is a user
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            # this kees it from saving it into the database
            newtodo = form.save(commit=False)
            # we dont want other users making todos for other users
            newtodo.user = request.user
            # this will put it it into the data base
            newtodo.save()
            # redirect back to home page where they can see there todo
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad Data'})


def currenttodos(request):
    # This returns the objects request by the user instead of showing all of the objects ex. all()
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})
