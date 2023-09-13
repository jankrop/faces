from django import template
register = template.Library()


@register.filter('list')
def make_list(value):
	return ', '.join(value)
