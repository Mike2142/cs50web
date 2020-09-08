from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Watchlist

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def categories_view(request):
    categories = Listing.objects.order_by('category').values('category').distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def category_view(request, category):
    listings = Listing.objects.filter(category = category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

def watchlist_view(request, username):
    if request.method == "POST" and request.POST["watchlist_title"]:
        watchlist_title = request.POST["watchlist_title"]
        watchlist_username = request.POST["watchlist_username"]
        watchlist_check = Watchlist.objects.filter(watchlist_user = username, watchlist_title = watchlist_title)
        if (not watchlist_check ):
            watch_item = Watchlist(watchlist_user = watchlist_username, watchlist_title = watchlist_title)
            watch_item.save()
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(watchlist_user = watchlist_username)
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(watchlist_user = username)
        })

def listing_view(request, title):

    target_listing = Listing.objects.get(title = title )
    comments = Comment.objects.filter(listing__title = title)

    if request.method == "POST" and request.POST.get('comment', ''):
        username = request.POST.get("username", '')
        comment = request.POST.get("comment", '')
        target_listing.comment_set.create(comment_user = username, comment_text = comment)
        # target_listing.save()

        return render(request, "auctions/listing.html", {
            "listing": target_listing,
            "comments": comments
        })

    if request.method == "POST" and request.POST.get('winner', ''):
        target_listing.active = False
        target_listing.save()
        return render(request, "auctions/listing.html", {
            "listing": target_listing,
            "comments": comments
        })

    if request.method == "POST":
        bid = request.POST["bid"]
        bidder = request.POST["bidder"]
        if int(bid) > target_listing.bid:
            target_listing.bid = bid
            target_listing.bidder = bidder
            target_listing.save()
        #else:
            # show message
        return render(request, "auctions/listing.html", {
            "listing": target_listing,
            "comments": comments
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": target_listing,
            "comments": comments
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

def create_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image = request.POST["image"] or '../static/auctions/placeholder-image.png'
        creator = request.POST["creator"]
        category = request.POST["category"]
        l = Listing(title = title, description = description, bid = bid, creator = creator, image = image, category = category)
        l.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")

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
