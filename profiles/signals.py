from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,FollowRequest

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=FollowRequest)
def post_save_send_request(sender,instance,created,**kwargs):
    if instance.receiver.privacy=='public':
        instance.approved=True

    if instance.approved==True:
        instance.sender.following.add(instance.receiver.user)
           