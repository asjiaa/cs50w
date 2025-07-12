from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import forms

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": reversed(Listing.objects.all())
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

# Specification 2 - Create Listings
@login_required
def create(request):
    form = forms.CreateForm(request.POST)
    if request.method == "POST":
        user = request.user
        if form.is_valid():
            data = form.cleaned_data
            listing = Listing.objects.create(
                category=data["category"],
                active=True,
                title=data["title"],
                description=data["description"],
                image=data["image"],
                lister=user
            )
            Bid.objects.create(
                amount=data["bid"],
                listing=listing,
                user=user
            )
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": form
    })


# Specification 4 - Listing Details
def listing(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    bid_form = forms.BidForm(request.POST)
    comment_form = forms.CommentForm(request.POST)
    comments = reversed(Comment.objects.all())
    error = False

    # 1 - Add/Remove Watchlist
    if request.method == "POST" and "add" in request.POST:
        listing.watchers.add(user)
        return redirect('listing', id=listing.id)
    
    elif request.method == "POST" and "remove" in request.POST:
        listing.watchers.remove(user)
        return redirect('listing', id=listing.id)
    
    # 2 - Bid
    elif request.method == "POST" and "bid" in request.POST:
        if bid_form.is_valid():
            data = bid_form.cleaned_data
            if (listing.count() == 1 and data["amount"] >= listing.price().amount) or (listing.count() > 1 and data["amount"] > listing.price().amount):
                error = False
                Bid.objects.create(
                    amount=data["amount"],
                    listing=listing,
                    user=user
                )
                return redirect('listing', id=listing.id)
            
            error = True
    
    # 3 - Close Auction
    elif request.method == "POST" and "close" in request.POST:
        listing.active = False
        if listing.price().user != listing.lister:
            listing.buyer = listing.price().user
        listing.save()
        return redirect('listing', id=listing.id)
    
    # 4 - Add Comment
    elif request.method == "POST" and "respond" in request.POST:
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(
                content=data["content"],
                listing=listing,
                user=user
            )
            comments = reversed(Comment.objects.all())
            return redirect('listing', id=listing.id)

    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing,
        "bid": bid_form,
        "comment": comment_form,
        "comments": comments,
        "error": error
    })


# Specification 5 - Watchlist
@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "list": reversed(request.user.watchlist.all())
    })


# Specification 6 - Categories
@login_required
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.Category
    })


# Specification 6 - Individual Category
@login_required
def category(request, category):
    return render(request, "auctions/category.html", {
        "categories": Listing.Category,
        "category": category,
        "listings": reversed(Listing.objects.all())
    })
