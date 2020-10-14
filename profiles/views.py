from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import Profile
from django.contrib import messages
from .forms import user_creation_form,extended_data_form,login_form
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
    
    context={
        'profile' : profile,
        'form1' : form1,
        'form2' : form2,
    }
    return render(request,'profiles/register.html',context)

def login_view(request):
    userform = login_form(request.POST or None)
    if request.method=='POST':
        if userform.is_valid():
            username = userform.cleaned_data.get('first_name')
            password = userform.cleaned_data.get('password')
            user = authenticate(username=username,password=password)  

            if user is not None:
                login(request,user)
                redirect('profiles:profile')
            else:
                messages.info(request,'username or password is incorrect')
        
    context={
        'userform': userform,
    }
    return render(request,'profiles/login.html',context)


def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    context ={
        'profile':profile,
    }
    return render(request,'profiles/my-profile',context)