from django.contrib import admin

from .models import User, Profile, Post, LikePost, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follow)

