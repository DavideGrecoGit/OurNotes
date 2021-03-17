from django import forms
from notes.models import User, Profile
from django.forms.fields import EmailField

class UserForm(forms.ModelForm):
    css = ' w-full bg-white border-black rounded-lg border-2 p-2 text-black font-medium'
    username = forms.CharField(label='Username')
    username.widget.attrs.update({'class':css,'placeholder': 'Username'})

    email = EmailField(label='Email')
    email.widget.attrs.update({'class':css,'placeholder': 'Email'})

    password = forms.CharField(widget=forms.PasswordInput())
    password.widget.attrs.update({'class':css, 'placeholder': 'Password'})
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profileImg',)


