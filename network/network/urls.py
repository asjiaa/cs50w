
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("compose", views.compose, name="compose"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("following", views.following, name="following"),

    # API Routes
    path("posts/<int:id>", views.posts, name="posts"),
    path("profile/posts/<int:id>", views.posts, name="posts"),
    path("following/posts/<int:id>", views.posts, name="posts"),
]
