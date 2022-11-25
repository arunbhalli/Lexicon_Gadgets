from django import template
from lexiconapp.models import BasketOrder

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = BasketOrder.objects.filter(user=user, complete=False)
        if qs.exists():
            return qs[0].items.count()
    return 0