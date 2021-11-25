
########################################################
#######             FUNCTION TEMPLATES
########################################################
from django import template

register= template.Library()

@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

@register.filter(name='replace')
def replace(value, args):
    key, key2 = args.split(',')
    return value.replace(key, key2)