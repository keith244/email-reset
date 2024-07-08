from django.shortcuts import render

# Create your views here.
def iregister(request):
    return render(request, 'user/register.html')

def ilogin(request):
    return render(request, 'user/login.html')