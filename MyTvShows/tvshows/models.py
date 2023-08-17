from django.contrib.auth import forms, get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from MyTvShows.tvshows.validators import check_name_capital_letter

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser


UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        unique=False,
    )

    username = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        validators=[MinLengthValidator(2)]
    )

    first_name = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        validators=[check_name_capital_letter]
    )

    last_name = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        validators=[check_name_capital_letter]
    )

    profile_picture = models.URLField(
        null=True,
        blank=True,
    )

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Review(models.Model):
    author = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )

    rating = models.IntegerField(
        null=False,
        blank=False,
        editable=True,
    )

    comment = models.TextField(
        null=False,
        blank=False,
    )

    def get_absolute_url(self):
        return reverse('index')


class Thread(models.Model):
    title = models.CharField(
        max_length=200
    )

    content = models.TextField(
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Reply by {self.author} on {self.thread.title}"


class TVShow(models.Model):
    user = models.ForeignKey(
                UserModel,
                on_delete=models.CASCADE,
                null=True,
                unique=False,
            )
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    tvmaze_id = models.CharField(max_length=20, unique=False)
    poster = models.URLField(max_length=300)
    seasons = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    episodes_watched = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=5000)


    def __str__(self):
        return self.title


class TemporarySearchResult(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        unique=False,
    )
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    tvmaze_id = models.CharField(max_length=20, unique=True)
    poster = models.URLField(max_length=300)
    seasons = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    episodes_watched = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.title


