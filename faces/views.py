from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import Post, User
from .forms import PostForm

def index(request):
	if request.user.is_authenticated:
		return render(request, 'home.html', {})
	else:
		return render(request, 'index.html', {})


@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = Post(content=form.cleaned_data['content'], author=request.user, date=datetime.utcnow())
			post.save()
			return HttpResponseRedirect(reverse('index'))
	else:
		form = PostForm()

	return render(request, 'create_post.html', {'form': form})


@login_required
def profile(request, username):
	user = get_object_or_404(User, username=username)
	return render(request, 'profile.html', {'user': user})


def post(request, username, identifier):
	user = get_object_or_404(User, username=username)
	post_object = get_object_or_404(Post, author=user, identifier=identifier)
	return render(request, 'post.html', {'post': post_object})
