import re
from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Create_Post,Profile,Comment

class Login_User_Form(AuthenticationForm):
    class Meta:
        fields = ['username','password']


def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

class Sign_Up_Form(UserCreationForm):   
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200,widget=forms.EmailInput)
    password1 = forms.CharField(max_length=20,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise forms.ValidationError("Invalid email format. Please enter a valid email address.")
        elif User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return email  
    

    def UppercaseValidator(self):
        password1 = self.cleaned_data.get('password1')
        if not re.search('[A-Z]', password1):
            raise forms.ValidationError("The password must contain at least 1 uppercase letter, A-Z.")
        return password1

    
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


"""Comment form"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']   
        labels = {
            "body": ""
        }
