# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm, LoginForm
from .models import CustomUser
from django import forms


class CustomUserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = ""
        self.fields['password'].label = ""

    login = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def login(self, *args, **kwargs):

        return super(CustomUserLoginForm, self).login(*args, **kwargs)





class CustomUserCreationForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def save(self, request):
    
        user = super(CustomUserCreationForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")




