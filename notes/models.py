from django.db import models
from django.template.defaultfilters import slugify
import os

# Create your models here.
class Category(models.Model):
    categoryName = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.categoryName

def user_imgs(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return os.path.join(os.path.join("uploads",'user_{0}'.format(instance.id)),os.path.join("profile_imgs", filename))

def user_notes(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return os.path.join(os.path.join("uploads",'user_{0}'.format(instance.id)),os.path.join("notes", filename))

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    profileImgs = models.ImageField(upload_to = user_imgs)
    
    def __str__(self):
        return self.username

class StudyGroup(models.Model):
    groupName = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=500, blank=True)
    rules = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.groupName)
        super(StudyGroup, self).save(*args, **kwargs)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='founder')
    members = models.ManyToManyField(User, related_name='members')

    def __str__(self):
        return self.groupName

class Url(models.Model):
    link = models.URLField()
    label = models.CharField(max_length=255)
    
    studyGroup = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

class Note(models.Model):
    noteName = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, blank=True)
    date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to = user_notes)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploadedBy')
    studyGroup = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

    rates = models.ManyToManyField(User, through='rates_notes', through_fields=('note', 'user'))

    def __str__(self):
        return self.noteName

class rates_notes(models.Model):

    rating = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username +" rates the note: "+ self.note.noteName +" "+ str(self.rating)

class Comment(models.Model):
    text = models.TextField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter') 
    replyTo = models.ForeignKey('self', null=True, blank= True,on_delete=models.CASCADE, related_name='parent')
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    rates = models.ManyToManyField(User, through='rates_comments', through_fields=('comment', 'user'))

    def __str__(self):
        return self.user.username+"("+self.note.noteName+"): "+self.text

class rates_comments(models.Model):

    rating = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username +" rates the comment: "+ self.comment.text +" "+ str(self.rating)
