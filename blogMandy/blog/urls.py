from django.urls import path
from . import views as v
app_name = 'blog'

urlpatterns = [
    path('home/',v.listviews,name='home'),
    path('home/create_post/',v.create_post,name='create_post'),
    path('home/update_post/<int:post_id>/',v.update_post,name='update_post'),
    path('home/delete_post/<int:post_id>/',v.delete_post,name='delete_post'),
    path('home/create_category/',v.create_category,name='create_category'),
]