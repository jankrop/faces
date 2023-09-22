from django import template
register = template.Library()


from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from markdown2 import markdown
from datetime import datetime, timezone


@register.filter('markdown')
def parse_markdown(value):
	value = conditional_escape(value).replace('&#x27;', "'").replace('&quot;', '"')
	return mark_safe(markdown(value, extras={
		'fenced-code-blocks': None,
		'code-friendly': None,
		'smarty-pants': None,
		'html-classes': {
			'pre': 'bg-body-tertiary border rounded p-3'
		}
	}))


@register.filter
def safe_id(value):
	return value.replace('-', '$')
