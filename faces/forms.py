from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['content']


class SearchForm(forms.Form):
	q = forms.CharField(label='Search query', max_length=150)


class CommentForm(forms.Form):
	content = forms.CharField(label='Comment', widget=forms.Textarea)


class RegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
