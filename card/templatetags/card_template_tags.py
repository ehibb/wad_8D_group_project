from django import template
from card.models import Category, FlashCardSet

register = template.Library()

@register.inclusion_tag('card/categories.html')
def get_category_list(current_category=None):
    return {"categories": Category.objects.all(),
            "current_category": current_category}

@register.inclusion_tag('card/cardsets.html')
def get_cardset_list():
    return {"cardsets":FlashCardSet.objects.all()}