from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice


class Class(models.Model):
	name = models.CharField(max_length=4)

	def __str__(self):
		return self.name


class User(AbstractUser):
	interests_choices = [
		('coding', 'Coding'),
		('writing', 'Writing'),
		('painting', 'Painting'),
		('photography', 'Photography'),
		('gaming', 'Gaming'),
		('reading', 'Reading'),
		('soccer', 'Soccer'),
		('technology', 'Technology'),
		('history', 'History'),
		('travelling', 'Travelling'),
	]

	friend_requests = models.ManyToManyField('self', symmetrical=False)
	friends = models.ManyToManyField('self')
	klass = models.ForeignKey(Class, blank=True, null=True, on_delete=models.SET_NULL)
	interests = models.JSONField(default=list, blank=True, null=True)

	def __str__(self):
		return self.username


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField()
	content = models.TextField()
	identifier = models.CharField(max_length=2)
	likes = models.ManyToManyField(User, related_name='liked_posts')

	def __generate_base64_identifier(self):
		chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-'
		is_unique = False
		while not is_unique:
			new_id = choice(chars) + choice(chars)
			is_unique = not Post.objects.filter(author=self.author, identifier=new_id).exists()
		return new_id

	def save(self, *args, **kwargs):
		if not self.identifier:
			self.identifier = self.__generate_base64_identifier()
		super().save(*args, **kwargs)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField()
	content = models.TextField()
	identifier = models.CharField(max_length=2)
	likes = models.ManyToManyField(User, related_name='liked_comments')
	response_to = models.ForeignKey(
		'self', on_delete=models.CASCADE, blank=True, null=True, related_name='responses'
	)

	def __generate_base64_identifier(self):
		chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-'
		is_unique = False
		while not is_unique:
			new_id = choice(chars) + choice(chars)
			is_unique = not Comment.objects.filter(post=self.post, identifier=new_id).exists()
		return new_id

	def save(self, *args, **kwargs):
		if not self.identifier:
			self.identifier = self.__generate_base64_identifier()
		super().save(*args, **kwargs)
