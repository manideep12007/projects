from django.urls import path
from .views import * 
app_name = 'users'
urlpatterns = [
    path('register/',register_form,name='register'),
    path('login/',login_form,name='login'),
    path('logout/',logout_form,name='logout'),
]