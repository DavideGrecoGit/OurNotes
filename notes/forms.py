from enum import Flag, unique
from django import forms
from notes.models import Category, Comment, Note, StudyGroup, Url, User, Profile
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
    groupName = forms.CharField()
    groupName.widget.attrs.update({'class':css,'placeholder': 'Group name'})

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    category.widget.attrs.update({'class':css})

    description = forms.CharField(widget=forms.Textarea, required=False)
    description.widget.attrs.update({'class':css,'placeholder': 'Insert a description here...', 'rows':8, 'cols':15})

    rules = forms.CharField(widget=forms.Textarea, required=False)
    rules.widget.attrs.update({'class':css,'placeholder': 'Insert rules here...', 'rows':6, 'cols':15})

    class Meta:
        model = StudyGroup
        fields = ('groupName','description','rules','category',)


class NoteForm(forms.ModelForm):
    noteName = forms.CharField()
    noteName.widget.attrs.update({'class':css,'placeholder': 'Note Name'})

    description = forms.CharField(widget=forms.Textarea, required=False)
    description.widget.attrs.update({'class':css,'placeholder': 'Insert a description here...', 'rows':4, 'cols':15})

    file = forms.FileField(label='Select a file', help_text='max. 42 megabytes')

    class Meta:
        model = Note
        fields = ('noteName', 'description', 'file',)

class UrlForm(forms.ModelForm):
    link = forms.CharField()
    link.widget.attrs.update({'class':css,'placeholder': 'Link'})
    
    label = forms.CharField()
    label.widget.attrs.update({'class':css,'placeholder': 'Link label'})

    class Meta:
        model = Url
        fields = ('link', 'label',)

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)
    text.widget.attrs.update({'class':css,'placeholder': 'Write a comment here...', 'rows':4, 'cols':15})

    class Meta:
        model = Comment
        fields = ('text', )


