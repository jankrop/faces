from django.urls import path
from faces_app import fed_views


urlpatterns = [
    path('@<slug:username>/exists', fed_views.user_exists)
]
