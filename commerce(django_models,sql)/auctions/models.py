from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    bid = models.IntegerField(default='0')
    bidder = models.CharField(default='none' ,max_length=64)
    creator = models.CharField(default='none' ,max_length=64)
    image = models.CharField(max_length=1000)
    category = models.CharField(default='misc', max_length=64)
    active = models.BooleanField(default=True)

class Bid(models.Model):
    bid_user = models.CharField(max_length=64)
    size = models.IntegerField()

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_user = models.CharField(max_length=64)
    comment_text = models.CharField(max_length=64)

class Watchlist(models.Model):
    watchlist_user = models.CharField(max_length=64)
    watchlist_title = models.CharField(max_length=64)