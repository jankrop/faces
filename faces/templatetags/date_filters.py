from django import template
register = template.Library()

import dateutil.parser


@register.filter
def from_iso(value):
	return dateutil.parser.isoparse(value).date()
