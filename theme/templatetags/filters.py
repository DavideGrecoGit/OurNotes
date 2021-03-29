from notes.models import Comment, Profile, rates_comments, rates_notes
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
def getUpVotesComment(comment):
    upVotes = rates_comments.objects.filter(rating=1, comment=comment).count()
    return upVotes

@register.filter
def getDownVotesComment(comment):
    DownVotes = rates_comments.objects.filter(rating=0, comment=comment).count()
    return DownVotes

@register.filter
def getUpVoteCommentImg(comment, user):
    default_img = "/static/icons/upVote_empty.png"
    try:
        vote = rates_comments.objects.get(rating=1, comment=comment, user=user)
        if(vote):
            return "/static/icons/upVote.png"
        
        return default_img

    except:
        return default_img

@register.filter
def getDownVoteCommentImg(comment, user):
    default_img = "/static/icons/downVote_empty.png"
    try:
        vote = rates_comments.objects.get(rating=0, comment=comment, user=user)
        if(vote):
            return "/static/icons/downVote.png"
        
        return default_img

    except:
        return default_img


@register.filter
def getUpVotesNote(note):
    upVotes = rates_notes.objects.filter(rating=1, note=note).count()
    return upVotes

@register.filter
def getDownVotesNote(note):
    DownVotes = rates_notes.objects.filter(rating=0, note=note).count()
    return DownVotes

@register.filter
def getUpVoteNoteImg(note, user):
    default_img = "/static/icons/upVote_empty.png"
    try:
        vote = rates_notes.objects.get(rating=1, note=note, user=user)
        if(vote):
            return "/static/icons/upVote.png"
        
        return default_img

    except:
        return default_img

@register.filter
def getDownVoteNoteImg(note, user):
    default_img = "/static/icons/downVote_empty.png"
    try:
        vote = rates_notes.objects.get(rating=0, note=note, user=user)
        if(vote):
            return "/static/icons/downVote.png"
        
        return default_img

    except:
        return default_img
