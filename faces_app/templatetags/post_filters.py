from django import template
register = template.Library()


from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from markdown2 import markdown


@register.filter('markdown')
def parse_markdown(value):
	value = conditional_escape(value).replace('&#x27;', "'").replace('&quot;', '"')
	return mark_safe(markdown(value, extras=['fenced_code_blocks', 'code_friendly', 'smarty_pants'])[:-1].replace('\n', '<br>'))
