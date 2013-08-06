from django import template
from django.db import models
register = template.Library();
def loadAttr(value,arg):
    if hasattr(value,arg):
        attr = getattr(value,str(arg));
        if isinstance(attr,models.Model):
            return attr.getDisplay();
        else:
            return attr;
def get_range(value,arg):
    return range(0,int(value));
register.filter('loadAttr',loadAttr);
register.filter('get_range',get_range);
