from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None,followers=0,following=0,post=0,image=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, followers=followers,followings=following,post=post,image=image)
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user


class Custom_User(AbstractBaseUser,PermissionsMixin):
    followers=models.PositiveIntegerField(null=True)
    followings=models.PositiveIntegerField(null=True)
    post=models.PositiveIntegerField(null=True)
    bio=models.TextField(null=True)
    name=models.CharField(max_length=30,unique=True)
    objects = CustomUserManager()
    email=models.CharField(max_length=40,unique=True)
    image=models.ImageField(null=True,blank=True,upload_to="image/")
    objects=CustomUserManager()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

class Posts(models.Model):
    user=models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    name = models.CharField(max_length=50)
    create=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Comment_db(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    user=models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    name=models.TextField()
    comment=models.TextField()


class Follow(models.Model):
    follower = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name="following")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Chat_Room(models.Model):
    user1=models.ForeignKey(Custom_User,on_delete=models.CASCADE,related_name="user1")
    user2=models.ForeignKey(Custom_User,on_delete=models.CASCADE,related_name="user2")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('user1','user2')
class Chat_Room_Message(models.Model):
    room=models.ForeignKey(Chat_Room,on_delete=models.CASCADE)
    sender=models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    context=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)




