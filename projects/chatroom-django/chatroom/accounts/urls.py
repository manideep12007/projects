from django.urls import path
from . import views as v 

urlpatterns = [
    path("user/login/",v.login_user,name="login"),
    path("user/logout/",v.logout_user,name="logout"),
    path("user/signup/",v.signup_user,name="signup"),
    path("user/profile/view/<int:pk>/",v.profile_view,name="profile_view"),
    path("user/profile/update/<int:pk>/",v.update_profile,name="profile_update"),
]