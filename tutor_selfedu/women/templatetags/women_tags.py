from django import template
from django.http import Http404
from django.db.models.aggregates import Count
from women.models import *

register = template.Library()

@register.simple_tag()
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=None):
    if not sort:
        cats = Category.objects.annotate(Count('women'))
    else:
        cats = Category.objects.annotate(Count('women')).order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('women/list_menu.html')
def show_menu(request):
    menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Add Page', 'url_name': 'add_page'},]
    return {'menu': menu, 'request': request}

@register.inclusion_tag('women/list_posts.html')
def show_posts(filter=None):
    if not filter:
        posts = Women.objects.filter(is_published=True)
    else:
        posts = Women.objects.filter(cat_id=filter, is_published=True)
    if len(posts) == 0:
        raise Http404()
    return {'posts': posts}