from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    author_user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

    def update_rating(self):
        post_rating_t = 0
        comment_rating_t = 0
        post_comment_rating_t = 0

        post_qset = Post.objects.filter(post_author = self)
        for i in post_qset:
            post_rating_t += i.post_rating

        comment_qset = Comment.objects.filter(comment_user = self.author_user)
        for i in comment_qset:
            comment_rating_t += i.comment_rating

        post_comment_qset = Comment.objects.filter(comment_post__post_author = self)
        for i in post_comment_qset:
            post_comment_rating_t += i.comment_rating

        self.author_rating = post_rating_t * 3 + comment_rating_t + post_comment_rating_t
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    article = 'ART'
    news = 'NEW'

    TYPE = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=3, choices=TYPE, default=article)
    post_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.post_title}: {self.post_text[:20]}'

    def like(self):
        self.post_rating +=1
        self.save()

    def dislike(self):
        self.post_rating -=1
        self.save()

    def preview(self):
        if len(self.post_text) < 124:
            prew = self.post_text
        else:
            prew = self.post_text[:124] + '...'
        return prew

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating +=1
        self.save()

    def dislike(self):
        self.comment_rating -=1
        self.save()



