from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = []


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='likes')
    hate = models.ManyToManyField(User, related_name='hates')

    def add_tmp_attr(self, user):
        self.like_pressed = user in self.like.all()
        self.hate_pressed = user in self.hate.all()

        self.like_description = f'({self.like.count()})추천'
        self.hate_description = f'({self.hate.count()})비추천'
        return self
