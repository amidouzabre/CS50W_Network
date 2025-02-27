from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "network/index.html", context={
        'posts':posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post_new(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
        print(post)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


def profile(request, username):
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    is_following = profile_user.is_followed_by(request.user)

    return render(request, "network/profile.html", context={
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following
    })


def follow_or_unfollow(request, username):
    profile_user = User.objects.get(username=username)
    if request.method == "POST":
        if request.POST["follow"] == "Follow":
            request.user.follow(profile_user)
        else:
            request.user.unfollow(profile_user)
        return HttpResponseRedirect(reverse("profile", args=[username]))
    else:
        return HttpResponseRedirect(reverse("profile", args=[username]))