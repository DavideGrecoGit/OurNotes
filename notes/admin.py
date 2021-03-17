from django.contrib import admin
from notes.models import Category, Comment, Note, StudyGroup, Url, Profile, rates_comments, rates_notes

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(StudyGroup)
admin.site.register(Url)
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(rates_comments)
admin.site.register(rates_notes)

