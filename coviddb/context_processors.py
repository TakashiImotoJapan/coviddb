from django.conf import settings
from django.template.defaulttags import register
import re
from django.urls import reverse, NoReverseMatch

from coviddb.models import State

def areas(request):
   return {'AREA_DIC': settings.AREA_DIC, 'STATE_DIC': {}}

def age_list(request):
   return {'AGE_LIST': settings.AGE_LIST}

def chart_color(request):
   return {'CHART_COLOR': settings.CHART_COLOR}

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def state_list(things):
    states = list(State.objects.values_list('romam', 'jp', flat=False).filter(disp=1))
    return states

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''

@register.simple_tag(takes_context=True)
def menu_open(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'menu-open'
    return ''