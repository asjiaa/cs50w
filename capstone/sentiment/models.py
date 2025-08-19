from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Topic(models.Model):
    topic = models.CharField(max_length=200)
    start = models.DateField()
    end = models.DateField()

    def serialize(self):
        return {
            "topic": self.topic,
            "start": self.start.strftime("%b %d %Y"),
            "end": self.end.strftime("%b %d %Y")
        }

class Log(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    search = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    uri = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    snippet = models.TextField(blank=True)
    headline = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
    topics = models.ManyToManyField("Topic", related_name="articles")

    def serialize(self):
        return {
            "uri": self.uri,
            "url": self.url,
            "snippet": self.snippet,
            "headline": self.headline,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "sentiment": {
                "compound": self.sentiment.compound,
                "pos": self.sentiment.pos,
                "neg": self.sentiment.neg,
                "neu": self.sentiment.neu
            }
        }

class Sentiment(models.Model):
    article = models.OneToOneField("Article", on_delete=models.CASCADE, related_name="sentiment")
    compound = models.FloatField()
    pos = models.FloatField()
    neg = models.FloatField()
    neu = models.FloatField()
