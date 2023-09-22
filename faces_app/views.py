from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from datetime import datetime
from .models import Post, User, Comment, Class
from .forms import PostForm, SearchForm, CommentForm, ReplyForm, RegistrationForm, UsernameChangeForm


# HELPER FUNCTIONS

def perform_like(request, obj):
	result = {}

	if obj.likes.contains(request.user):
		obj.likes.remove(request.user)
		result['actionType'] = 'dislike'
	else:
		obj.likes.add(request.user)
		result['actionType'] = 'like'

	obj.save()
	return result


# GENERAL VIEWS

def index(request):
	"""A view rendering login.html for non-users and home.html for users"""
	if request.user.is_authenticated:
		return render(request, 'home.html', {})
	else:
		return (LoginView.as_view())(request)


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
			query = form.cleaned_data['q']
			matches = User.objects.annotate(
				full_name=Concat('first_name', V(' '), 'last_name')
			).filter(
				Q(full_name__contains=query) |
				Q(username__contains=query)
			)
	form = SearchForm()
	return render(request, 'browse.html', {'form': form, 'matches': matches})


def class_list(request, classname):
	klass = get_object_or_404(Class, name=classname)
	members = klass.user_set.order_by('last_name')
	return render(request, 'class.html', {'classname': classname, 'members': members})


def settings(request):
	return render(request, 'settings.html', {})


# ACCOUNT-RELATED VIEWS

def sign_in(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
	else:
		form = RegistrationForm()

	return render(request, 'registration/register.html', {'form': form})


def change_username(request):
	if request.method == 'POST':
		form = UsernameChangeForm(request.POST)
		if form.is_valid():
			request.user.username = form.cleaned_data['username']
			request.user.save()
			return HttpResponseRedirect(reverse('index'))
	else:
		form = UsernameChangeForm()

	return render(request, 'registration/username_change.html', {'form': form})


# POST-RELATED VIEWS

@login_required
def create_post(request):
	"""A view handling the PostForm form"""
	form = PostForm(request.POST)
	if form.is_valid():
		post_object = Post(content=form.cleaned_data['content'], author=request.user, date=datetime.utcnow())
		post_object.save()

	return HttpResponseRedirect(request.POST.get('path'))


@login_required
def post(request, username, identifier):
	"""A view rendering a page with a Post's data, comments and handling the CommentForm form"""
	post_object = get_object_or_404(Post, author__username=username, identifier=identifier)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment(
				post=post_object,
				author=request.user,
				date=datetime.utcnow(),
				content=form.cleaned_data['content'],
			)
			comment.save()
	form = CommentForm()

	return render(request, 'post.html', {'post': post_object, 'form': form, 'reply_form': ReplyForm()})


@login_required
def like(request, username, identifier):
	"""
	A view for managing a Post's likes and returning the undertaken action (like or dislike) as a JSON.
	It should be called using AJAX.
	"""
	post_object = get_object_or_404(Post, author__username=username, identifier=identifier)
	return JsonResponse(perform_like(request, post_object))


@login_required
def delete_post(request, username, identifier):
	"""A view for deleting a Post"""
	if request.user.username == username:
		get_object_or_404(Post, author__username=username, identifier=identifier).delete()
		return HttpResponseRedirect(reverse('profile', args=[request.user]))
	else:
		return HttpResponseForbidden('You must be the author of a post to delete it.')


@login_required
def edit_post(request, username, identifier):
	"""A view for editing a Post"""
	if request.user.username == username:
		post_object = get_object_or_404(Post, author__username=username, identifier=identifier)
		form = PostForm(request.POST)
		if form.is_valid():
			post_object.content = form.cleaned_data['content']
		post_object.save()
		return HttpResponseRedirect(request.POST.get('path'))
	else:
		return HttpResponseForbidden('You must be the author of a post to edit it.')


@login_required
def get_feed(request):
	try:
		start, end = int(request.GET['start']), int(request.GET['end'])
	except (KeyError, ValueError):
		return HttpResponseBadRequest('The request must have two integer params: start and end.')
	posts = Post.objects.filter(author__in=request.user.friends.all()).order_by('-date')[start:end]
	return render(request, 'widgets/feed.html', {'posts': posts})


# COMMENT-RELATED VIEWS

@login_required
def reply(request, username, post_id, comment_id):
	form = ReplyForm(request.POST)
	if form.is_valid():
		post_obj = get_object_or_404(Post, author__username=username, identifier=post_id)
		comment = get_object_or_404(Comment, post=post_obj, identifier=comment_id)
		reply_obj = Comment(
			post=post_obj,
			author=request.user,
			date=datetime.utcnow(),
			content=form.cleaned_data['content'],
			response_to=comment
		)
		reply_obj.save()
	return HttpResponseRedirect(reverse('post', args=[username, post_id]))


@login_required
def like_comment(request, username, post_id, comment_id):
	"""
	A view for managing a Comment's likes and returning the undertaken action (like or dislike) as a JSON.
	It should be called using AJAX.
	"""
	comment_object = get_object_or_404(
		Comment, post__author__username=username, post__identifier=post_id, identifier=comment_id
	)
	return JsonResponse(perform_like(request, comment_object))


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


def friend_list(request):
	friends = request.user.friends.all()
	return render(request, 'friends.html', {'friends': friends})


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


# INTEREST_RELATED VIEWS

@login_required
def change_interests(request):
	request.user.interests = dict(request.POST).get('interests')
	request.user.save()
	return HttpResponseRedirect(request.POST.get('path'))
