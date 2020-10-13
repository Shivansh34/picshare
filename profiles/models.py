from django.db import models
from django.contrib.auth.models import User

# Create your models here.
privacy_choices=(('public','public'),('private','private'))
request_choices=(('pending','pending'),('accepted','accepted'))

class Profile(models.Model):
    first_name = models.CharField(max_length=60,blank=True)
    last_name = models.CharField(max_length=60,blank=True)
    date_of_birth = models.DateField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(default='avatar.png',upload_to='avatars/')
    bio = models.TextField(max_length=255)
    privacy = models.CharField(max_length=7,choices=privacy_choices,default='private')

    #Relationships
    user = models.OneToOneField(User,name='user',on_delete=models.CASCADE)
    following = models.ManyToManyField('self',blank=True,related_name='following',through='FollowRequest')#user object follows

    
    

class FollowRequest(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='senders')
    receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receivers')
    sentdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=request_choices,max_length=8,default='pending')


"""
create a request receive function in class for followrequest
if public auto approve

"""