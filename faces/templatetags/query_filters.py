from django import template
register = template.Library()


@register.filter('contains')
def query_contains(value, arg):
	return value.contains(arg)
