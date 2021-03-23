from django_component import Library, Component

register = Library()

@register.component
class Message(Component):
    template = "base_components/message.html"

@register.component
class Nav_link(Component):
    template = "base_components/nav_link.html"


#Show_group
@register.component
class Sidebar(Component):
    template = "show_group/sidebar.html"

@register.component
class Meetings(Component):
    template = "show_group/meetings.html"

@register.component
class Notes(Component):
    template = "show_group/notes/notes.html"

@register.component
class Comments(Component):
    template = "show_group/notes/comments.html"

@register.component
class Members(Component):
    template = "show_group/members.html"

#Forms
@register.component
class Form_field(Component):
    template = "base_components/forms/form_field.html"

@register.component
class Form_file(Component):
    template = "base_components/forms/form_file.html"

@register.component
class Form_error(Component):
    template = "base_components/forms/Form_error.html"

@register.component
class Form_btn(Component):
    template = "base_components/forms/form_btn.html"

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

