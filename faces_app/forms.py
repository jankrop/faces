from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from .models import User, Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['content']


class SearchForm(forms.Form):
	q = forms.CharField(label='Search query', max_length=150)


class CommentForm(forms.Form):
	content = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'rows': '1', 'placeholder': 'Comment'}))

	helper = FormHelper()
	helper.label_class = 'visually-hidden'
	helper.layout = Layout(
		FieldWithButtons(
			'content',
			StrictButton('<i class="bi bi-send-fill"></i>', type='submit', css_class='btn-primary'))
	)


class ReplyForm(CommentForm):
	content = forms.CharField(label='Reply', widget=forms.Textarea(attrs={'rows': '1', 'placeholder': 'Reply'}))


class RegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'klass']
