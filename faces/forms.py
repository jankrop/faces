from django import forms
from .models import Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['content']


class SearchForm(forms.Form):
	query = forms.CharField(label='Search query', max_length=150)
