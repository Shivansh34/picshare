from django.urls import path
from .views import my_post_view,explore_view,like_unlike_post,addcomment,edit,add,explore_view

urlpatterns = [
    path('',explore_view,name='allposts'),
    path('explore/',explore_view,name='explore'),
    path('myposts/',my_post_view,name='myposts'),
    path('like/',like_unlike_post,name='like_unlike'),
    path('addcomment/',addcomment,name='add_comment'),
    path('<pk>/edit/',edit.as_view(),name='edit'),
    path('add/',add,name='add'),
 #   path('deletecomment/<pk>',deletecomment,name='delete_comment'),
]