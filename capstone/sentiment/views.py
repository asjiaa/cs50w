import calendar
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import util
from . import forms

from .models import User, Topic, Log, Article, Sentiment

# Create your views here.


def index(request):
    topics = util.get_topics

    return render(request, "sentiment/index.html", {
        "form": forms.SearchForm(),
        "topics": topics,
        "user": request.user
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
            return render(request, "sentiment/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sentiment/login.html")


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
            return render(request, "sentiment/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sentiment/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sentiment/register.html")
    

def sentiment(request):
    form = forms.SearchForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            query = ' '.join(data["query"].strip().lower().split())
            start = date(int(data["start_year"]), int(data["start_month"]), 1)
            end = date(
                int(data["end_year"]),
                int(data["end_month"]),
                calendar.monthrange(int(data["end_year"]), int(data["end_month"]))[1]
            )
            if end < start:
                return JsonResponse({"error": "End date cannot be earlier than start date."}, status=400)
            
            # Update topic model if new topic query
            try:
                topic = Topic.objects.get(
                    topic=query,
                    start=start,
                    end=end
                )
            except Topic.DoesNotExist:
                topic = Topic.objects.create(
                    topic=query,
                    start=start,
                    end=end
                )
            
            # Update articles model if new article
            articles = util.get_articles(topic.topic, topic.start, topic.end)
            if not articles:
                topic.delete()
                return JsonResponse({"error": "No results found."}, status=404)
            
            for article in articles:
                try:
                    subject = Article.objects.get(
                        uri=article["uri"]
                    )
                except Article.DoesNotExist:
                    subject = Article.objects.create(
                        uri=article["uri"],
                        url=article["url"],
                        snippet=article["snippet"],
                        headline=article["headline"],
                        timestamp=article["timestamp"],
                    )

                    sentiment = util.get_sentiment(
                        subject.headline + "\n" + subject.snippet
                    )
                    Sentiment.objects.create(
                        article=subject,
                        compound=sentiment["compound"],
                        pos=sentiment["pos"],
                        neg=sentiment["neg"],
                        neu=sentiment["neu"]
                    )
                    
                subject.topics.add(topic)
                subject.save()
            
            # Update search logs
            user = request.user
            if user.is_authenticated:
                Log.objects.create(
                    user=user,
                    search=topic.topic
                )
                
            # Return relevant article sentiment data
            response = []
            results = Article.objects.filter(
                topics=topic
            )
            for result in results:
                response.append(result.serialize())

            return JsonResponse({
                "topic": topic.serialize(),
                "articles": response
            })

    return JsonResponse({
        "error": "POST request required."
    }, status=400)


@csrf_exempt
def search(request):
    user = request.user

    if user.is_authenticated:
        if request.method == "GET":
            log = Log.objects.filter(
                user=user
            ).order_by(
                "-timestamp"
            ).values_list("search", flat=True)
            response = list(dict.fromkeys(log))
            return JsonResponse({
                "response": response
            })
        
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    
    return JsonResponse({"response": []})
