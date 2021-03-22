from django_component import Library, Component

register = Library()

@register.component
class Message(Component):
    template = "base_components/message.html"

@register.component
class Nav_link(Component):
    template = "base_components/nav_link.html"

@register.component
class Form_field(Component):
    template = "forms/form_field.html"

@register.component
class Group_buttons(Component):
    template = "base_components/Group_buttons.html"


# CARDS
@register.component
class Card_child(Component):
    template = "base_components/cards/card_child.html"

@register.component
class Card_parent(Component):
    template = "base_components/cards/card_parent.html"

@register.component
class Card_user(Component):
    template = "base_components/cards/card_user.html"

