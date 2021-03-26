from notes.models import Comment, Profile, rates_comments
from django.template.defaulttags import comment, register

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
    
@register.filter
def getLikes(comment):
    #comment = Comment.objects.get(id=comment_id)
    likes = rates_comments.objects.filter(rating=1, comment=comment).count()
    return likes

@register.filter
def getUnLikes(comment):
    #comment = Comment.objects.get(id=comment_id)
    not_likes = rates_comments.objects.filter(rating=0, comment=comment).count()
    return not_likes
