from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

# Specification 1 - Models

# 1 - Auction Listings

class Listing(models.Model):
    class Category(models.TextChoices):
        FASHION = "Fashion"
        ENTERTAINMENT = "Entertainment"
        ELECTRONIC = "Electronic"
        HOME = "Home"
        MISCELLANEOUS = "Miscellaneous"
        
    category = models.CharField(max_length=64, choices=Category)
    active = models.BooleanField()
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="buys")
    watchers = models.ManyToManyField(User, null=True, blank=True, related_name="watchlist")

    def count(self):
        return self.bids.count()

    def price(self):
        return self.bids.order_by("-amount", "-created").first()

# 2 - Bids
class Bid(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")

# 3 - Listing Comments
class Comment(models.Model):
    content = models.TextField(max_length=500)
    created = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity")
