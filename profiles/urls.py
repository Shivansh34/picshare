from django.urls import path
from .views import profile_view,login_view,register,my_profile_view,my_post_view,follow_requests,profile_edit,send_request,logout_view
from posts.views import  profile_posts_view,profile_followers_views

urlpatterns = [
    path('',my_profile_view,name='profile'),
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('waiting/',follow_requests,name='followrequest'),
    path('edit/',profile_edit,name='profileedit'),
    path('follow/',send_request,name="sendrequest"),
    path('feed/',profile_followers_views,name='feed'),
    path('<pk>/',profile_view,name='otherprofiles'),
    path('<pk>/posts/',profile_posts_view,name='otherprofileposts'),
    #path('<pk>/delete',profile_delete,name='profile_delete')
]