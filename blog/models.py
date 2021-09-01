from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (False, "Draft"),
    (True, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updatedOn = models.DateTimeField(auto_now=True)
    content = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(choices=STATUS, default=True)

    class Meta:
        ordering = ['-createdOn']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-createdOn']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
