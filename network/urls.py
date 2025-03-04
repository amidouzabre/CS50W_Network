from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/add/", views.post_add, name="post_add"),
    path("post/edit/<int:post_id>", views.post_edit, name="post_edit"),
    path("post/like/<int:post_id>", views.like_or_dislike, name="like_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/edit/<str:username>", views.edit_profile,name="edit_profile"),
    path("profile/follow/<int:user_id>", views.follow_or_unfollow, name="follow"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)