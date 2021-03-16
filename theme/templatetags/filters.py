from django.template.defaulttags import register

@register.filter
def getItem(dictionary, key):
    return dictionary.get(key)
