from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *

# Register your models here.
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(Story)