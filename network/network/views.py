import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import forms

from .models import User, Post

# Specification 2 - All Posts

def index(request):
    posts = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request, "network/index.html", {
        "form": forms.ComposeForm(),
        "posts": page_obj
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


# Specification 1 - New Post

@login_required
def compose(request):
    form = forms.ComposeForm(request.POST)
    user = request.user
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                poster=user,
                content=data["content"]
            )
    return HttpResponseRedirect(reverse("index"))


# Specification 3 - Profile Page

def profile(request, id):
    user = User.objects.get(pk=id)
    posts = user.posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request, "network/profile.html", {
        "owner": user,
        "posts": page_obj
    })


@login_required
def follow(request, id):
    user = request.user
    owner = User.objects.get(pk=id)
    if request.method == "POST":
        if owner != user:
            if owner not in user.following.all():
                user.following.add(owner)
            else:
                user.following.remove(owner)
    return redirect("profile", id=id)


# Specification 4 - Following

@login_required
def following(request):
    user = request.user
    posts = Post.objects.filter(
        poster__in=user.following.all()
    ).order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request, "network/following.html", {
        "posts": page_obj
    })


@csrf_exempt
@login_required
def posts(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    user = request.user

    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            if (post.poster != user):
                return JsonResponse({"error": "Cannot edit another user's post."}, status=404)
            post.content = data["content"]
        if data.get("likes") is id:
            if user not in post.likes.all():
                user.liked.add(post)
            else:
                user.liked.remove(post)
        post.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
