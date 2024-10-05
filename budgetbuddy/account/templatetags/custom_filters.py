from django import template

register = template.Library()

@register.filter
def starts_with(value, arg):
    """Check if value starts with arg."""
    return value.startswith(arg)