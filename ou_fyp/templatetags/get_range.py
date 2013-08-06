from django import template
register = template.Library();
def get_range(value,arg=None):
    return range(1,int(value)+1);
register.filter('get_range',get_range);
