from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    commenter = models.ForeignKey('auth.User', related_name='commenter', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    
class Like(models.Model):
    liker = models.ForeignKey('auth.User', related_name='liker', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.liker.username


class Photo(models.Model):
    photo = models.ImageField()

    def __str__(self):
        return str(self.photo)


class Activity(models.Model):
    influncer = models.ForeignKey('auth.User', related_name='influncer', on_delete=models.CASCADE)
    influnced = models.ForeignKey('auth.User', related_name='influnced', on_delete=models.CASCADE)
    action = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action


class Post(models.Model):
    likes = models.ManyToManyField(Like, related_name='likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='comments', blank=True)
    photoes = models.ManyToManyField(Photo, related_name='photoes', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(blank=True, default='post')
    saved = models.BooleanField(blank=True, null=True, default=False)
    saving_user_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.caption
    
    
class Profile(models.Model):
    user = models.ForeignKey('auth.User', related_name='user' ,on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    isShop = models.BooleanField(blank=True, null=True, default=False)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    
    def __str__(self):
        return self.user.username


class Story(models.Model):
    photoes = models.ManyToManyField(Photo, related_name='stories', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='stories', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner)