from django.shortcuts import render,redirect
from .models import Post,Comment,Like
from profiles.models import Profile
from .forms import PostForm,CommentForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
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
    likes = profile.liked.all()

    context={
        'profile' : profile ,
        'posts' : allposts ,
        'likes' : likes ,
    }
    return render(request,'posts/feed.html',context)

def like_unlike_post(request):
    if request.method=='POST':
        print('dun')
        post_pk = request.POST.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(user=request.user) 
        if profile in post.likes.all():
            Like.objects.get(post=post,liker=profile).delete()
            post.likes.remove(profile)
        else:
            post.likes.add(profile)
            obj = Like.objects.create(post=post,liker=profile)
            obj.save()
        
    return redirect('posts:feed')

def addcomment(request):
    if request.method=='POST':
        post_pk = request.POST.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(user=request.user)
        data= request.POST.get('comment')
        comment = Comment.objects.create(post=post,commentor=profile,data=data)
        comment.save()
    return redirect('posts:feed')

class edit(UpdateView):
    form_class = PostForm
    template_name = 'posts/editpost.html'
    model = Post
    success_url = reverse_lazy('posts:edit')

    def form_valid(self, form):
        profile = profile.objects.get(user=self.request.user)
        if form.instance.op==profile:
            return super().form_valid(form)
        else:
            form.add_error(None,"You are not the author of this post")
            return super().form_invalid(form)

def add(request):
    post_form = PostForm(request.POST or None,request.FILES or None)
    if request.method=="POST":
        profile = Profile.objects.get(user=request.user)
        if post_form.is_valid():
            newpost = post_form.save(commit=False)
            newpost.op = profile
            newpost.save()
            return redirect('posts:feed')
        else:
            print(post_form.errors.as_data())
            
    context ={
        'post_form' : post_form,
    }
    return render(request,'posts/add.html',context)

