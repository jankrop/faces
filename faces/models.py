from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice


class User(AbstractUser):
	friend_requests = models.ManyToManyField('self', symmetrical=False)
	friends = models.ManyToManyField('self')

	def __str__(self):
		return self.username


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField()
	content = models.TextField()
	identifier = models.CharField(max_length=2)
	likes = models.ManyToManyField(User, related_name='liked_posts')
	comments = models.JSONField(default=list)  # comment format: {author, date, content, likes[], responses[]}

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
