from django.urls import path
from .views import profile_view,login_view,register

urlpatterns = [
    path('myprofile/',profile_view,name='profile'),
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    #path('<pk>/delete',profile_delete,name='profile_delete')
]