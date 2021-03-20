from django_component import Library, Component

register = Library()

@register.component
class Card_children(Component):
    template = "base_components/card_children.html"

@register.component
class Card_parent(Component):
    template = "base_components/card_parent.html"

@register.component
class Card_user(Component):
    template = "base_components/card_user.html"

@register.component
class Message(Component):
    template = "base_components/message.html"

@register.component
class Nav_link(Component):
    template = "base_components/nav_link.html"

@register.component
class Register_field(Component):
    template = "register/register_field.html"

