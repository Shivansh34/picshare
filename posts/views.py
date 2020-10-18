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

def explore_view(request):
    profile = Profile.objects.get(user=request.user)
    allposts = Post.objects.all()

    context={
        'profile' : profile ,
        'posts' : allposts ,
        'nbar': 'explore',
    }
    return render(request,'posts/feed.html',context)

def like_unlike_post(request):
    if request.method=='POST':
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
    to_url = request.POST.get('current_url')
    return redirect(to_url)

def addcomment(request):
    if request.method=='POST':
        post_pk = request.POST.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(user=request.user)
        data= request.POST.get('comment')
        comment = Comment.objects.create(post=post,commentor=profile,data=data)
        comment.save()
    to_url = request.POST.get('current_url')
    return redirect(to_url)

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
            return redirect('posts:explore')
        else:
            print(post_form.errors.as_data())
            
    context ={
        'post_form' : post_form,
        'nbar' :'add',
    }
    return render(request,'posts/add.html',context)

def profile_posts_view(request,pk):
    profile=Profile.objects.get(pk=pk)
    posts = Post.objects.filter(op=profile)
    prof = Profile.objects.get(user=request.user)

    context={
        'profile' : prof ,
        'posts' : posts ,
        'nbar': 'home',
    }
    return render(request,'posts/feed.html',context)

def profile_followers_views(request):
    profile = Profile.objects.get(user=request.user)
    allposts = Post.objects.all()
    posts = []
    for post in allposts:
        if post.op.user in profile.following.all():
            posts.append(post)
    prof = Profile.objects.get(user=request.user)

    context={
        'profile' : prof ,
        'posts' : posts ,
        'nbar': 'home',
    }
    return render(request,'posts/feed.html',context)
