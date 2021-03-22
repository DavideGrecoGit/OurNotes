from notes.models import Profile
from django.template.defaulttags import register

@register.filter
def getItem(dictionary, key):
    return dictionary.get(key)

@register.filter
def getImage(user):
    profile = Profile.objects.get(user=user)
    if(profile):
        if(profile.profileImg):
            return profile.profileImg.url

    return False
    
