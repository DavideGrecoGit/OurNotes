# myapp/templatetags/mycomponents.py

from django_component import Library, Component

register = Library()

@register.component
class Card_children(Component):
    template = "base_components/card_children.html"

    #class Media:
        #css = {"all": ["../../theme/static/css/styles.css"]}
        #js = ["myapp/card.js"]

@register.component
class Card_parent(Component):
    template = "base_components/card_parent.html"

@register.component
class Nav_link(Component):
    template = "base_components/nav_link.html"

