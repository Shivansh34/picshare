from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .models import Profile
from .forms import user_creation_form,extended_data_form
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
    return render(request,'profiles\register.html',context)