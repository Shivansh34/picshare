from django.contrib import admin
from .models import Profile,FollowRequest

# Register your models here.
admin.site.register(Profile)
admin.site.register(FollowRequest)