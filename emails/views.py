from django.shortcuts import render
# Create your views here.
def password_reset_request(request):
    return render(request,'emails/password_reset.html')