from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Create_Post,Profile



class Login_User_Form(AuthenticationForm):
    class Meta:
        fields = ['username','password']



class Sign_Up_Form(UserCreationForm):   
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200)
    password1 = forms.CharField(max_length=50,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')



class User_Post_Creation(forms.ModelForm):
    class Meta:
        model = Create_Post
        fields = ['post_img','caption']



class User_Profile_Creation(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
 
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']
 
 

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']