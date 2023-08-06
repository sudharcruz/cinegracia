from django import template

register = template.Library()

@register.simple_tag
def future_tag():
    return "This is a future tag!"
