from django.http import HttpResponse
from .models import User


def user_exists(request, username):
    if User.objects.filter(username=username).exists():
        return HttpResponse('true')
    else:
        return HttpResponse('false')
