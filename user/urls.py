from django.urls import path
from . import views
#add urls here
urlpatterns= [
    path('register/',views.iregister, name='register'),
    path('login/',views.ilogin, name='login'),
    path('logout/',views.ilogout,name='logout'),
    path('index/',views.index, name='index')
]