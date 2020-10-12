from django.db import models

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=60,blank=True)
    last_name = models.CharField(max_length=60,blank=True)
    date_of_birth = models.DateField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(default='avatar.png',upload_to='avatars/')