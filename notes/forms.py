from django import forms
from notes.models import StudyGroup, User, Profile
from django.forms.fields import EmailField

css = ' w-full bg-white border-black rounded-lg border-2 p-2 text-black font-medium'

class UserForm(forms.ModelForm):
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


class GroupForm(forms.ModelForm):
    groupName = forms.TimeField()
    groupName.widget.attrs.update({'class':css,'placeholder': 'Group Name'})

    description = forms.TextInput()
    description.attrs.update({'class':css,'placeholder': 'Insert a description here...'})

    rules = forms.TextInput()
    rules.attrs.update({'class':css,'placeholder': 'Insert rules here...'})

    class Meta:
        model = StudyGroup
        exclude = ('slug',)



