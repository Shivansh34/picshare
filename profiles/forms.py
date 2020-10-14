from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class user_creation_form(UserCreationForm):
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=False)
    class Meta:
        model= User
        fields = ('first_name','last_name','password1','password2')

    def save(self,commit=True):
        user =super().save(commit=False)
        user.username=self.cleaned_data['first_name']

        if commit:
            user.save()
        return user

class extended_data_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','avatar','privacy')

class login_form(forms.Form):
    first_name = forms.CharField(max_length=50,required=True)
    password = forms.PasswordInput()
    