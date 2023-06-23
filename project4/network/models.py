from django.contrib.auth.models import AbstractUser
from django.db import models

import math
from datetime import date, datetime


def time_since_date(specified_date):
    now = datetime.now(specified_date.tzinfo)
    delta = now - specified_date
    seconds = delta.total_seconds()
    if seconds < 60:
        seconds = math.floor(seconds)
        seconds = 1 if seconds == 0 else seconds
        return f"{seconds:.0f}s ago"
    minutes = seconds / 60
    if minutes < 60:
        minutes = math.floor(minutes)
        return f"{minutes:.0f}m ago"
    hours = minutes / 60
    if hours < 24:
        hours = math.floor(hours)
        return f"{hours:.0f}h ago" if hours == 1 else f"{hours:.0f}hs ago"
    return specified_date.strftime("%d/%m/%Y")


class User(AbstractUser):
    users_following = models.ManyToManyField('User', blank=True, null=True, related_name='followed_by')
    watchlist = models.ManyToManyField('Post', blank=True, null=True, related_name='watched_by')

    def __str__(self):
        return self.username

    def like_post(self, post):
        post.liked_by.add(self)
        post.save()

    @property
    def number_followers(self):
        return len(self.followed_by.all())

    @property
    def number_following(self):
        return len(self.users_following.all())

    @property
    def number_post_watching(self):
        return len(self.watchlist)


class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    liked_by = models.ManyToManyField('User', null=True, blank=True, related_name='liked_posts')
    content = models.TextField()

    def __str__(self):
        content = self.content if len(self.content) <= 20 else self.content[:18] + "..."
        date = self.date_created.strftime("%Y-%m-%d %H:%M")
        return f"{self.user.username}: {content} ({date})"

    @property
    def time_since_creation(self):
       return time_since_date(self.date_created)

    @property
    def time_since_modification(self):
       return time_since_date(self.date_modified)

    @property
    def number_likes(self):
        return len(self.liked_by.all())

    def serialize(self):
        date_modified = self.date_modified.strftime("%b %d %Y, %I:%M %p") if isinstance(self.date_modified, (date, datetime)) else ""
        return {
            "id": self.id,
            "user": self.user.username,
            "liked_by": [user.username for user in self.liked_by.all()],
            "number_likes": self.number_likes,
            "content": self.content,
            "date_modified": date_modified,
            "date_created": self.date_created.strftime("%b %d %Y, %I:%M %p"),
            "time_since_creation": self.time_since_creation
        }


