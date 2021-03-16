from django.shortcuts import render
from django.http import HttpResponse, request
from django.template.defaulttags import comment
from notes.models import Comment, Note, StudyGroup, Category, Url

# Create your views here.
def search(request):
    context_dict = {}

    category_list = Category.objects.order_by('categoryName')

    groups = {}
    for category in category_list:
        group = StudyGroup.objects.filter(category = category)
        groups[category.categoryName] = group

    context_dict['groups'] = groups
    context_dict['categories'] = category_list

    return render(request, 'search.html', context=context_dict)

def faq(request):
    context_dict = {}
    return render(request, 'faq.html', context=context_dict)

def show_group(request, studyGroup_slug):
    context_dict = {}

    try:
        # Get studyGroup related to this slug, if any
        studyGroup = StudyGroup.objects.get(slug=studyGroup_slug)
        studyGroup.rules = studyGroup.rules.replace("[","")
        studyGroup.rules = studyGroup.rules.replace("]","")
        studyGroup.description = studyGroup.description.replace("[","")
        studyGroup.description = studyGroup.description.replace("]","")

        studyGroup.rules = studyGroup.rules.replace("'","")
        studyGroup.description = studyGroup.description.replace("'","")

        studyGroup.rules = studyGroup.rules.replace(",","")
        studyGroup.description = studyGroup.description.replace(",","")


        context_dict['group'] = studyGroup

        context_dict['rules'] = "not empty"
        if(studyGroup.rules==""):
            context_dict['rules'] = None

        context_dict['description'] = "not empty"
        if(studyGroup.description==""):
            context_dict['description'] = None

        # Get urls
        urls = Url.objects.filter(studyGroup=studyGroup)
        context_dict['urls'] = urls

        # Get notes
        notes = Note.objects.filter(studyGroup=studyGroup)
        context_dict['notes'] = notes

        # Get comments
        comments = {}
        for note in notes:
            comment = Comment.objects.filter(note = note)
            comments[note.noteName] = comment

        context_dict['comments'] = comments

        #Get members        
        members = studyGroup.members.all()
        context_dict['members'] = members

    except StudyGroup.DoesNotExist:
        # if there are no associated groups
        # the template will display the "no category" message for us.
        context_dict['group'] = None
        context_dict['notes'] = None

    return render(request, 'show_group.html', context=context_dict)