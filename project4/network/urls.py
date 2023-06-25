
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts-page", views.posts_page, name="posts_page"),
    path("like-unlike-post", views.like_unlike_post, name="like_unlike_post"),
    path("view-post", views.view_post, name="view_post"),
    path("user/<str:username>/", views.view_user, name="view_user"),
    path("follow-unfollow-user", views.follow_unfollow_user, name="follow_unfollow_user"),
    path("add-new-post", views.add_new_post, name="add_new_post"),
    path("following", views.following, name="following"),
    path("submit-post-change", views.submit_post_change, name="submit_post_change"),
]
