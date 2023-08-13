from django import template
register = template.Library()


@register.filter('contains')
def query_contains(value, arg):
	return value.contains(arg)


@register.filter('non_reply')
def non_reply_comments(value):
	return value.filter(response_to=None)
