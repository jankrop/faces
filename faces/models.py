from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	def __str__(self):
		return self.username


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	id = models.CharField(max_length=4, primary_key=True)
	date = models.DateTimeField()
	content = models.TextField()
