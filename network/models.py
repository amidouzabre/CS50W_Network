from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    user_img = models.ImageField(upload_to='user_images/', default="user_images/blank_user_img.png")

    def is_followed_by(self, user):
        return self.followers.filter(follower=user).exists()


    def follow(self, user):
        if not self.is_followed_by(user):
            Follow.objects.create(follower=user, following=self)
            return True
        return False
    
    def unfollow(self, user):
        if self.is_followed_by(user):
            Follow.objects.get(follower=user, following=self).delete()
            return True
        return False


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
