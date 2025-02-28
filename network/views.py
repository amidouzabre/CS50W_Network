from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, LikePost


def index(request):
    posts_list = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        for post in posts_list:
            post.user_liked = post.likes.filter(user=request.user).exists()

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
def post_add(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.user != post.user:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        data = json.loads(request.body) # Parse request body as JSON
        post.content = data.get("content")  # Get content from parsed JSON
        post.save()  # Save the updated post
        return JsonResponse({"content": post.content})  # Return updated content as JSON

    return HttpResponseRedirect(reverse("index"))



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
    

@login_required
def like_or_dislike(request, post_id):
    post = Post.objects.get(id=post_id)
    user_liked = post.likes.filter(user=request.user).exists()
    
    if user_liked:
        like = LikePost.objects.filter(user=request.user, post=post)
        like.delete()
        action = "disliked"
    else:
        like = LikePost.objects.create(user=request.user, post=post)
        like.save()
        action = "liked"

    return JsonResponse({"content": action})