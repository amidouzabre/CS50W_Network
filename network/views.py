from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
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



@login_required
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
    posts_list = Post.objects.filter(user=profile_user).order_by('-created_at')


    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)



    is_following = profile_user.is_followed_by(request.user) if request.user.is_authenticated else False

    return render(request, "network/profile.html", context={
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following
    })


@login_required
def follow_or_unfollow(request, username):
    profile_user = User.objects.get(username=username)
    is_following = profile_user.is_followed_by(request.user)

    print("is_following", is_following)
    print("profile_user", profile_user)

    if(is_following):
        print("unfollow request")
        unfollow = Follow.objects.get(follower=request.user, following=profile_user)    
        unfollow.delete()
    else:    
        print("follow request")
        follow = Follow.objects.create(follower=request.user, following=profile_user)
        follow.save()
    return HttpResponseRedirect(reverse("profile", args=[username]))
    


@login_required
def following(request):
    following = Follow.objects.filter(follower=request.user)
    posts_list = Post.objects.filter(user__in=[f.following for f in following]).order_by('-created_at')


    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    
    return render(request, "network/following.html", context={
        'following': following,
        'posts': posts
    })
    