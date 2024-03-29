from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
register = template.Library()

from faces_app.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404


@register.filter(needs_autoescape=True)
def full_name(value, autoescape=True):
	if isinstance(value, str):
		value = get_object_or_404(User, username=value)
	elif not isinstance(value, User):
		return

	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x
	result = f'<a href="{reverse("profile", args=[value])}">' \
			 f'{esc(value.first_name)} {esc(value.last_name)} @{value}' \
			 '</a>'
	return mark_safe(result)

