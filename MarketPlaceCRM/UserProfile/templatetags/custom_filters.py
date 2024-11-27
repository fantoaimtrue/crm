<<<<<<< HEAD
from django import template

register = template.Library()

@register.filter
def mask_token(value):
    """Показывает только первые 4 символа токена, остальное заменяет на звёздочки."""
    if value and len(value) > 4:
        return value[:4] + '*' * (len(value) - 4)
    return value
=======
from django import template

register = template.Library()

@register.filter
def mask_token(value):
    """Показывает только первые 4 символа токена, остальное заменяет на звёздочки."""
    if value and len(value) > 4:
        return value[:4] + '*' * (len(value) - 4)
    return value
>>>>>>> 8792f0a8650c8e4af713ed61e06e632a3406ea43
