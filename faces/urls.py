"""faces URL Configuration

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
from faces_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.sign_in, name='register'),
    path('admin/', admin.site.urls),
    path('create/', views.create_post, name='create_post'),
    path('feed/', views.get_feed, name='feed'),
    path('@<slug:username>', views.profile, name='profile'),
    path('@<slug:username>/friend', views.friend, name='friend'),
    path('@<slug:username>/accept', views.accept_friend_request, name='accept_friend_request'),
    path('@<slug:username>/decline', views.decline_friend_request, name='decline_friend_request'),
    path('@<slug:username>/<slug:identifier>', views.post, name='post'),
    path('@<slug:username>/<slug:identifier>/like', views.like, name='like'),
    path('@<slug:username>/<slug:identifier>/delete', views.delete_post, name='delete_post'),
    path('@<slug:username>/<slug:identifier>/edit', views.edit_post, name='edit_post'),
    path('@<slug:username>/<slug:post_id>/<slug:comment_id>/reply', views.reply, name='reply'),
    path('@<slug:username>/<slug:post_id>/<slug:comment_id>/like', views.like_comment, name='like_comment'),
    path('browse/', views.browse, name='browse'),
    path('fed/', include('faces_app.fed_urls')),
]
