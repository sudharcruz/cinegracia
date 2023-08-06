from django import template

register = template.Library()

@register.filter
def add_size(value, size):
    return f"{value}/w{size}"
