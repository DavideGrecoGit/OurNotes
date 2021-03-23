from notes.models import Profile, User
from django.template.defaulttags import register

@register.filter
def getItem(dictionary, key):
    return dictionary.get(key)

@register.filter
def getImage(user):

    default_img = "/static/icons/user_default.png"

    try:
        profile = Profile.objects.get(user=user)
        if(profile):
            if(profile.profileImg):
                return profile.profileImg.url
        
        return default_img

    except:
        return default_img

@register.filter
def isMember(group, user):
    if(user in group.members.all()):
        return True
    return False
    
