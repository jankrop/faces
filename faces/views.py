from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from datetime import datetime
from .models import Post, User
from .forms import PostForm, SearchForm, CommentForm


# GENERAL VIEWS

def index(request):
	"""A view rendering index.html for non-users and home.html for users"""
	if request.user.is_authenticated:
		return render(request, 'home.html', {})
	else:
		return render(request, 'index.html', {})


@login_required
def profile(request, username):
	"""A view rendering a user's profile page"""
	user = get_object_or_404(User, username=username)
	return render(request, 'profile.html', {'viewed_user': user})


@login_required
def browse(request):
	"""A view handling the SearchForm form"""
	matches = []
	if request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['q'].lower()
			matches = User.objects.filter(username__contains=query)
	form = SearchForm()
	return render(request, 'browse.html', {'form': form, 'matches': matches})


# POST-RELATED VIEWS

@login_required
def create_post(request):
	"""A view handling the PostForm form"""
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
def post(request, username, identifier):
	"""A view rendering a page with a Post's data, comments and handling the CommentForm form"""
	user = get_object_or_404(User, username=username)
	post_object = get_object_or_404(Post, author=user, identifier=identifier)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = {
				'author': request.user.username,
				'date': datetime.utcnow().isoformat(),
				'content': form.cleaned_data['content'],
				'likes': [],
				'responses': [],
			}
			post_object.comments.append(comment)
			post_object.save()
	else:
		form = CommentForm()

	comments = post_object.comments
	return render(request, 'post.html', {'post': post_object, 'form': form, 'comments': comments})


@login_required
def like(request, username, identifier):
	"""
	A view for managing a Post's likes and returning the undertaken action (like or dislike) as a JSON.
	It should be called using AJAX.
	"""
	user = get_object_or_404(User, username=username)
	post_object = get_object_or_404(Post, author=user, identifier=identifier)
	result = {}

	if post_object.likes.contains(request.user):
		post_object.likes.remove(request.user)
		result['actionType'] = 'dislike'
	else:
		post_object.likes.add(request.user)
		result['actionType'] = 'like'

	post_object.save()
	return JsonResponse(result)


# FRIEND-RELATED VIEWS

@login_required
def friend(request, username):
	"""
	A view for managing friendships. It can execute 3 actions depending on the users' relationship:
		1. End friendship if users are already friends
		2. Revoke a friend request if one is already sent
		3. Send a friend request if there is no relationship between the users.
	"""
	if username != request.user.username:
		user = get_object_or_404(User, username=username)
		if user.friends.contains(request.user):
			user.friends.remove(request.user)
		elif user.friend_requests.contains(request.user):
			user.friend_requests.remove(request.user)
		else:
			user.friend_requests.add(request.user)
		user.save()
	return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required
def accept_friend_request(request, username):
	"""A view for accepting a friend request"""
	try:
		user = request.user.friend_requests.get(username=username)
	except User.DoesNotExist:
		raise Http404
	request.user.friend_requests.remove(user)
	request.user.friends.add(user)
	request.user.save()
	return HttpResponseRedirect(reverse('index'))


@login_required
def decline_friend_request(request, username):
	"""A view for declining a friend request"""
	user = get_object_or_404(User, username=username)
	request.user.friend_requests.remove(user)
	return HttpResponseRedirect(reverse('index'))
