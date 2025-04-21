from django.urls import path
from . import views as v 

urlpatterns = [
    path("",v.home,name="home"),
    path("room/<int:pk>/",v.room,name="room"),
    path("room/create/",v.create_room,name="create_room"),
    path("room/update/<int:pk>/",v.update_room,name="update_room"),
    path("room/delete/<int:pk>/",v.delete_room,name="delete_room"),
    path("room/message/delete/<int:pk>/",v.delete_message,name="delete_message"),
    path("room/message/update/<int:pk>/",v.update_message,name="update_message"),
    path("hashtag/create/",v.create_hashtag,name="create_hashtag"),
    path("hashtag/delete/<int:pk>/",v.delete_hashtag,name="delete_hashtag"),
]