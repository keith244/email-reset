from django.shortcuts import render, redirect, get_object_or_404
from .models import myUser
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def iregister(request):
    if request.method == 'POST':
        username  = request.POST['username']
        email     = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #Password validation
        if password1 != password2 :
            messages.error(request, 'Passwords don\'t match')
            return render(request, 'user/register.html')
        
        #check for existing email
        if myUser.objects.filter( email=email ).exists():
            messages.error(request, 'A user with that email already exists. Choose another.')
            return render( request, 'user/register.html' )
        
        #check for existing username
        if myUser.objects.filter (username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'users/register.html')
        
        user= myUser.objects.create (
            username = username, 
            email    = email,
        )
        user.set_password(password1)
        user.is_active = True
        user.save()
        return redirect('login')
    
    return render (request, 'user/register.html')

def ilogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('index')
        else:
            if myUser.objects.filter(username=username).exists():
                messages.error(request, 'Invalid credentials provided.')
            else:
                print('eeeeeee')
                messages.error(request, f'Account with username "{username}" does not exist. Please create an account.')
            return redirect('login')  # Redirect back to login page
    else:
        return render(request, 'user/login.html')

def ilogout(request):
    logout (request)
    return redirect ('login')

@login_required (login_url='login')
def index(request):
    return render( request, 'user/index.html')