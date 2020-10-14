from django.urls import path
from .views import my_post_view,feed_view

urlpatterns = [
    path('feed/',feed_view,name='feed'),
    path('myposts/',my_post_view,name='myposts'),
]