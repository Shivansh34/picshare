from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.

class Post(models.Model):
    caption = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='posts/',validators=[FileExtensionValidator(['jpg','png','jpeg'])],blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    op = models.ForeignKey(Profile,blank=False,on_delete=models.CASCADE,related_name='posts')
    

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,related_name='likers')
    liker = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='liked')
    created = models.DateTimeField(auto_now_add=True)
