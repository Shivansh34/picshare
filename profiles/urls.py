from django.urls import path
from .views import profile_view,profile_delete

urlpatterns = [
    path('profile/<pk>/',profile_view,name='profile'),
    path('profile/<pk>/delete',profile_delete,name='profile_delete')
]