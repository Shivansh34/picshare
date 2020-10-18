from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Profile,FollowRequest
from django.contrib import messages
from .forms import user_creation_form,extended_data_form,login_form,edit_form
from django.contrib.auth.models import User
from posts.models import Post
from django.shortcuts import get_object_or_404
# Create your views here.

def register(request):
    form1 = user_creation_form(request.POST or None)
    form2 = extended_data_form(request.POST or None,request.FILES or None)

    if request.method=='POST':
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            
            profile = form2.save(commit=False)#create a form model object but doesn't save it
            
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.user = user

            username = form1.cleaned_data.get('username')
            password = form1.cleaned_data.get('password1')
            user = authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('profiles:profile')
        else:
            print('prob')
    context={
        'form1' : form1,
        'form2' : form2,
    }
    return render(request,'profiles/register.html',context)

def login_view(request):
    userform = login_form(request.POST or None)
    if request.method=='POST':
        if userform.is_valid():
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')
            user = authenticate(username=username,password=password)  

            if user is not None:
                login(request,user)
                return redirect('profiles:profile')
            else:
                messages.info(request,'username or password is incorrect')
        
    context={
        'userform': userform,
    }
    return render(request,'profiles/login.html',context)

def my_profile_view(request):
    pk = request.user.pk
    return redirect('profiles:otherprofiles',pk)

def profile_view(request,pk):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    allow = 0
    pending = 0 
    personal = Profile.objects.get(user=request.user)
    cunt = FollowRequest.objects.filter(receiver=profile,status='accepted').count()
    if FollowRequest.objects.filter(receiver=profile,sender=personal,status='pending').count()>0:
        pending = 1
    if user==request.user:
        personal=0
        allow = 1
    elif profile.privacy=='public':
        allow = 1
    context ={
        'profile':profile,
        'nbar':'profile',
        'allow':allow,
        'personal': personal,
        'followers':cunt,
        'pending':pending,
    }
    return render(request,'profiles/profile.html',context)

def my_post_view(request):
    profile = Profile.objects.get(user=request.user)
    pk = profile.pk
    return redirect('profiles:otherprofileposts',pk)


def follow_requests(request):
    profile = Profile.objects.get(user=request.user)
    followrequests = FollowRequest.objects.filter(receiver=profile,status='pending')
    context ={
        'followrequests':followrequests,
        'nbar':'waiting'
    }
    if request.method=="POST":
        pk = request.POST.get('freqpk')
        frequest = FollowRequest.objects.get(pk=pk)
        if 'accepted' in request.POST:
            frequest.status='accepted'
            frequest.save()
        elif 'declined' in request.POST:
            frequest.delete()

    return render(request,'profiles/requests.html',context)

def profile_edit(request):
    instance = get_object_or_404(Profile,user=request.user)
    profileform = edit_form(request.POST or None,request.FILES or None,instance=instance)
    if request.method=="POST":
        if profileform.is_valid():
            profile = profileform.save()
            user = User.objects.get(pk=request.user.pk)
            user.first_name = profile.first_name
            user.last_name = profile.last_name
            user.save()
            return redirect('profiles:profile')
        else:
            messages.info(request,'illegal data')
    context={
        'profileform':profileform,
    }
    return render(request,'profiles/editprofile.html',context)

def send_request(request):
    if request.method=='POST':
        profile_pk = request.POST.get('profile_pk')
        to_url = request.POST.get('current_url')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=profile_pk)
        print(to_url)
        if 'unfollow' in request.POST:
            req = FollowRequest.objects.get(sender=sender,receiver=receiver)
            sender.following.remove(receiver.user)
            sender.save()
            req.delete()
        elif 'pending' in request.POST:
            req = FollowRequest.objects.get(sender=sender,receiver=receiver)
            req.delete()
        else:
            req = FollowRequest.objects.create(sender=sender,receiver=receiver)
            req.save()
    return redirect(to_url)

def logout_view(request):
    if request.method=='POST':
        if 'confirm' in request.POST:
            logout(request)
            return redirect('profiles:login')
        else:
            return redirect('profiles:profile')
    context ={
        'nbar':'logout'
    }
    return render(request,'profiles/logout.html',context)