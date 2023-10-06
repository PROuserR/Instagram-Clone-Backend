from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    my_id = models.ForeignKey('auth.User', related_name='my_id', on_delete=models.CASCADE)
    peer_id = models.ForeignKey('auth.User', related_name='peer_id', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content