from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def search(request):
    context_dict = {}
    return render(request, 'notes/search.html', context=context_dict)

def faq(request):
    context_dict = {}
    return render(request, 'notes/faq.html', context=context_dict)