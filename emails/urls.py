from django.urls import path
from . import views
#add urls here
urlpatterns= [
    path('password_reset/',views.password_reset_request, name='password_reset'),
    path('password_reset_confirm/<str:token>/', views.password_reset_confirm,name='password_reset_confirm'),
    # path('password_reset_email',views.)
]