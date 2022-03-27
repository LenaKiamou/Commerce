from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    context = {'listing': Listing.objects.filter(status=True), 'title': 'All active listings' }
    return render(request, "auctions/index.html", context)


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


@login_required
def create_view(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            if request.user.is_authenticated:
                new.owner = request.user
                new.save()
                return redirect("index")
    else:
        form = NewListing()

    context = {'form': form}
    return render(request, "auctions/create.html", context)


def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bid_user = None
    in_watchlist = None
    mine = None
    if request.user.is_authenticated:
        in_watchlist = request.user.watchlist_items.filter(id=listing_id)
        mine = listing.owner == request.user

    if Bids.objects.filter(listing=listing_id):
        bid_user = Bids.objects.filter(listing=listing_id).last().user 

    context = {'listing': listing, 'CommentForm': CommentForm(), 'comments': Comments.objects.filter(listing=listing_id), 
                'bid_form': BidForm(), 'bid': listing.current_bid, 'in_watchlist': in_watchlist, 'mine' : mine, 
                'winner': bid_user}
    return render(request, "auctions/listing.html", context)


def categories_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)


def category_view(request, category_id):
    context = {'listing': Listing.objects.filter(category=category_id, status=True),
             'title': f"Active listings under '{Category.objects.get(id=category_id).category}'"}
    return render(request, "auctions/index.html", context)


@login_required
def comment_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = CommentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.listing = listing
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            context = {'listing': listing, 'CommentForm': CommentForm(), 'comments': Comments.objects.filter(listing=listing_id)}
            return render(request, "auctions/listing.html", context)


@login_required
def create_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    offer = float(request.POST.get('value_offer'))
    if Bids.objects.filter(listing=listing_id):
        bid_user = Bids.objects.filter(listing=listing_id).last().user 
    if offer >= listing.starting_bid and (listing.current_bid is None or offer > listing.current_bid):
        listing.current_bid = offer
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.user = request.user
            bid.listing = listing
            bid.save()
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            context = {'listing': listing,'bid': listing.current_bid ,'bid_form': bid_form, 'bid_user': bid_user}
            return render(request, "auctions/listing.html", context)
    else:
        messages.warning(request, "You must bid a higher price!")
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            

@login_required
def closed(request, listing_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            listing = Listing.objects.get(id=listing_id)
            if request.user == listing.owner:
                listing.status = False
                listing.save()
                messages.warning(request, "Auction has closed!")
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def my_watchlist(request):
    if request.user.is_authenticated:
        context = {'listing': request.user.watchlist_items.all(), 'title': "My Watchlist"}
        return render(request, "auctions/index.html", context)


@login_required
def watchlist_view(request, listing_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            listing = Listing.objects.get(id=listing_id)
            if user.watchlist_items.filter(id=listing_id):
                user.watchlist_items.remove(listing)
            else:
                user.watchlist_items.add(listing)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))