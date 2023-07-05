from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice


class User(AbstractUser):
	def __str__(self):
		return self.username


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField()
	content = models.TextField()
	identifier = models.CharField(max_length=2)
	likes = models.ManyToManyField(User, related_name='liked_posts')

	def save(self, *args, **kwargs):
		if not self.identifier:
			chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-'
			is_unique = False
			while not is_unique:
				new_id = choice(chars) + choice(chars)
				is_unique = not Post.objects.filter(author=self.author, identifier=new_id).exists()
			self.identifier = new_id
		super().save(*args, **kwargs)
