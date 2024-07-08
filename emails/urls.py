from django.urls import path
from . import views
#add urls here
urlpatterns= [
    path('password_reset/',views.password_reset_request, name='password_reset'),
]