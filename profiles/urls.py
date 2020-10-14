from django.urls import path
from .views import profile_view,profile_delete

urlpatterns = [
    path('<pk>/',profile_view,name='profile'),
    path('register')
    #path('<pk>/delete',profile_delete,name='profile_delete')
]