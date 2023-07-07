"""faces2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from faces import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('create/', views.create_post, name='create_post'),
    path('@<slug:username>', views.profile, name='profile'),
    path('@<slug:username>/friend', views.friend, name='friend'),
    path('@<slug:username>/accept', views.accept_friend_request, name='accept_friend_request'),
    path('@<slug:username>/<slug:identifier>', views.post, name='post'),
    path('@<slug:username>/<slug:identifier>/like', views.like, name='like'),
    path('@<slug:username>/<slug:identifier>/delete', views.delete_post, name='delete_post'),
    path('browse/', views.browse, name='browse'),
]
