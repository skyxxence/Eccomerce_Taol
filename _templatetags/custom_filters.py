from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by arg."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Return 0 if either value or arg is not a number