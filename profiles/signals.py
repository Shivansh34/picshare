from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,FollowRequest

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance,first_name=instance.username)

@receiver(pre_save,sender=FollowRequest)
def pre_save_send_request(sender,instance,**kwargs):
    if instance.receiver.privacy=='public'and instance.status=='pending':
        instance.status='accepted'

@receiver(post_save,sender=FollowRequest)
def post_save_send_request(sender,instance,created,**kwargs):
    if instance.status=='accepted':
        instance.sender.following.add(instance.receiver.user)
        instance.sender.save()
    
    qs = instance.sender.following.all()
    print(instance.sender,qs)    

@receiver(post_save,sender=Profile)
def post_save_profile(sender,instance,created,**kwargs):
    if instance.privacy=='public':
        qs = FollowRequest.objects.filter(receiver=instance,status='pending')
        for req in qs:
            req.status='accepted'
            req.save()