from django import template
register = template.Library()

from datetime import datetime, timezone


@register.filter
def from_now(value):
	now = datetime.now(timezone.utc)
	delta = now - value
	if delta.days >= 365:
		years = delta.days // 365
		if years > 1:
			return f'{years} years ago'
		return 'a year ago'
	elif delta.days >= 30:
		months = delta.days // 30
		if months > 1:
			return f'{months} months ago'
		return 'a month ago'
	elif delta.days:
		if delta.days > 1:
			return f'{delta.days} days ago'
		return 'yesterday'
	elif delta.seconds >= 3600:
		hours = delta.seconds // 3600
		if hours > 1:
			return f'{hours} hours ago'
		return 'an hour ago'
	elif delta.seconds > 60:
		minutes = delta.seconds // 60
		if minutes > 1:
			return f'{minutes} minutes ago'
		return 'a minute ago'
	return 'just now'


