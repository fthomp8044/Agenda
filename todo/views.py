from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# For creating a new user
from django.contrib.auth.models import User

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        # create new User.Built in django object to help us makes it really easy to make user object.
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
        else:
            # Tell user the password didnt match
            print("hello")
