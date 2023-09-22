from django import template
register = template.Library()


from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from markdown2 import markdown
from datetime import datetime, tzinfo


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


@register.filter
def minutes_to_post_unlock(value):
	if not value.post_set.last(): return -999
	last_post_date = value.post_set.last().date
	return 600 - (datetime.now() - last_post_date).seconds // 60
