from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_since(date):
    if date:
        delta = timezone.now().date() - date
        return delta.days
    return 0
