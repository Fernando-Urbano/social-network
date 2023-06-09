from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post


def index(request):
    posts = Post.objects.order_by('-date_created')
    user = request.user
    return render(request, "network/index.html", {
        "user": user,
    })


@csrf_exempt
def posts_page(request):
    if request.method == "GET":
        # Handle GET request, if needed
        return JsonResponse({"message": "GET request received."})
    if request.method != "POST":
        return JsonResponse({
            "error": f"Request method provided ({request.method}) is not POST."
        }, status=400)
    data = json.loads(request.body)
    page_number = int(data.get("page_number", 1))
    posts_per_page = int(data.get("posts_per_page", 10))
    specification = data.get("specification", "all")
    if specification == "all":
        posts = Post.objects.order_by('-date_created').all()
    elif specification == "user":
        try:
            user_id = int(data.get("user_id"))
        except:
            return JsonResponse({
                "error": "User id must be specified and convertable into integer to address 'user' specification"
            }, status=400)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist: 
            return JsonResponse({"error": "User does not exist."}, status=400)
        posts = Post.objects.order_by('-date_created').filter(user=user)
    elif specification == "following":
        if not request.user.is_authenticated:
            return JsonResponse({
                "message": "No user is logged. Login to view the posts of following users."
            }, status=401)
        else:
            user = User.objects.get(pk=request.user_id)
            posts = Post.objects.order_by("-date_created").filter(user__in=user.users_following)
    elif specification == "watchlist":
        if not request.user.is_authenticated:
            return JsonResponse({
                "message": "No user is logged. Login to view your post's watchlist."
            }, status=401)
        else:
            user = User.objects.get(pk=request.user_id)
            posts = user.watchist
    else:
        return JsonResponse({
            "error": "Specification must be 'all', 'user', 'following' or 'watchlist'."
        }, status=401)
    if len(posts) == 0:
        return JsonResponse({
            "message": f"No posts found."
        }, status=201)
    start = (page_number - 1) * posts_per_page
    end = min(start + posts_per_page - 1, len(posts))
    try:
        page_posts = posts[start:end]
    except IndexError:
        last_page = (len(posts) // posts_per_page) + 1
        return JsonResponse({
            "error": f"{page_number:.0f} does not exist. Page {last_page} is the last page."
        }, status=400)
    return JsonResponse(
        {
            "number_pages": len(posts) // posts_per_page + 1,
            "posts": [post.serialize() for post in page_posts]
        },
    safe=False)
    

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
