from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from .models import User, Post


def index(request):
    user = request.user
    return render(request, "network/index.html", {
        "user": user,
    })


@csrf_exempt
def view_post(request):
    data = json.loads(request.body)
    post_id = int(data.get("post_id"))
    post = Post.objects.get(id=post_id)
    return JsonResponse(post.serialize(), safe=False)


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
        user_id = data.get("user_id", None)
        if user_id:
            try:
                user_id = int(user_id)
            except TypeError:
                return JsonResponse({
                    "error": "User id must be convertable to integer"
                }, status=400)
        username = data.get("username", None)
        if user_id is None and username is None:
            return JsonResponse({
                "error": "User id or username must be specified to address 'user' specification"
            }, status=400)
        try:
            if user_id:
                user = User.objects.get(pk=user_id)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=400)
        posts = Post.objects.order_by('-date_created').filter(user=user)
    elif specification == "following":
        if not request.user.is_authenticated:
            return JsonResponse({
                "message": "No user is logged. Login to view the posts of following users."
            }, status=401)
        else:
            user = User.objects.get(pk=request.user.id)
            posts = Post.objects.order_by("-date_created").filter(user__in=user.users_following.all())
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


@csrf_exempt
def like_unlike_post(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request body'}, status=400)
    post = Post.objects.get(id=post_id)
    user = request.user
    if post.liked_by.filter(id=user.id).exists():
        post.liked_by.remove(user)
        return JsonResponse({'message': f'Post {int(post_id)} unliked by {user.username}.'})
    else:
        post.liked_by.add(user)
        return JsonResponse({'message': f'Post {int(post_id)} liked by {user.username}.'})
    post.save()


@csrf_exempt
def submit_post_change(request):
    data = json.loads(request.body)
    user = request.user
    logging.info("Requested to submit change in post.")
    post_id = int(data.get('post_id'))
    logging.debug("Got post id")
    post = Post.objects.get(pk=post_id)
    if post.user != user:
        raise PermissionError(f"Logged user ({user.username}) is only allowed to change his own post.")
    post.content = data.get('new_content')
    post.save()
    return JsonResponse({'message': f"{user.username} edited post {post_id}."})


def view_user(request, username):
    logged_user = request.user
    try:
        user = User.objects.get(username=username)
    except:
        pass
    posts = Post.objects.filter(user=user)
    if logged_user.is_authenticated:
        following = logged_user.users_following.filter(pk=user.id).exists()
    else:
        following = None
    return render(request, 'network/user.html', {
        "searched_user": user,
        "posts": posts,
        "user": logged_user,
        "following": following
    })


def follow_unfollow_user(request):
    searched_user_id = int(request.POST["searched_user_id"])
    searched_user = User.objects.get(pk=searched_user_id)
    user = request.user
    if user.users_following.filter(pk=searched_user.id).exists():
        user.users_following.remove(searched_user)
        logging.info(f'{user.username} stopped following {searched_user.username}')
    else:
        user.users_following.add(searched_user)
        logging.info(f'{user.username} started following {searched_user.username}')
    user.save()
    return redirect('view_user', username=searched_user.username)


def add_new_post(request):
    user = request.user
    new_post_content = request.POST["new_post_content"]
    post = Post(user=user, content=new_post_content)
    post.save()
    return redirect('index')


def following(request):
    user = request.user
    return render(request, "network/index.html", {
        "user": user,
        "following_page": True
    })

