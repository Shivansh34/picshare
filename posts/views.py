from django.shortcuts import render
from .models import Post,Comment,Like
from profiles.models import Profile
from .forms import PostForm,CommentForm
# Create your views here.

def my_post_view(request):
    profile = Profile.objects.get(user=request.user)
    my_posts = profile.posts.all()
    context={
        'posts':my_posts,
    }
    return render(request,'posts/myposts.html',context)

def feed_view(request):
    profile = Profile.objects.get(user=request.user)
    allposts = Post.objects.all()
    context={
        'profile':profile,
        'posts':allposts,
    }
    return render(request,'posts/feed.html',context)