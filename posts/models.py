from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.

class Post(models.Model):
    caption = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='posts/',validators=[FileExtensionValidator(['jpg','png','jpeg'])],blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    op = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='posts')
    likes = models.ManyToManyField(Profile,blank=True,name='likes')
    objects= models.Manager()

    def __str__(self):
        return str(self.caption[:20])
    
    def num_likes(self):
        return self.likers.all().count()
    
    def num_comments(self):
        return self.comments.all().count()
    
    class Meta:
        ordering=('created',)

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,related_name='likers')
    liker = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='liked')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Comment(models.Model):
    commentor = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='comments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    data = models.CharField(max_length=100,blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)