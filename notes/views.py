from django.shortcuts import render
from django.http import HttpResponse
from notes.models import StudyGroup, Category

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