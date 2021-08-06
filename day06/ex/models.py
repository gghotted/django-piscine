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

        self.deleteable = self.deleteable_by(user)
        return self

    @property
    def like_description(self):
        return f'({self.like.count()})추천'

    @property
    def hate_description(self):
        return f'({self.hate.count()})비추천'

    '''
    user required properties: add attr user before call property
    '''
    @property
    def like_pressed(self):
        return self.user in self.like.all()

    @property
    def hate_pressed(self):
        return self.user in self.hate.all()

    @property
    def deleteable(self):
        return self.user.has_perm('ex.delete_tip') or self.author == self.user


def addusers(queryset, user, attrname='user'):
    def adduser(obj):
        setattr(obj, attrname, user)
        return obj

    return map(adduser, queryset)
