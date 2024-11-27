from django import template

register = template.Library()

@register.filter
def mask_token(value):
    """Показывает только первые 4 символа токена, остальное заменяет на звёздочки."""
    if value and len(value) > 4:
        return value[:4] + '*' * (len(value) - 4)
    return value
