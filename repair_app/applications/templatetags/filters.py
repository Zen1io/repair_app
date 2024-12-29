from django import template

register = template.Library()


@register.filter
def get_from_dict(dictionary, key):
    """Получить значение из словаря по ключу."""
    return dictionary.get(int(key), None)
