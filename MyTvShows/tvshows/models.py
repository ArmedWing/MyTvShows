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


class Show(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        unique=False,
    )

    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    image_url = models.URLField(
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=False,
        blank=False
    )

    day_of_airing = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name

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

    series = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        null=True
    )

    def get_absolute_url(self):
        return reverse('index')

class Genre(models.Model):
    Action = 'Action'
    Comedy = 'Comedy'
    Fantasy = 'Fantasy'
    SciFi = 'Sci-fi'
    Drama = 'Drama'
    Thriller = 'Thriller'
    Animated = 'Animated'

    CHOICES = (
        (Action, 'Action'),
        (Comedy, 'Comedy'),
        (Fantasy, 'Fantasy'),
        (SciFi, 'Sci-fi'),
        (Drama, 'Drama'),
        (Thriller, 'Thriller'),
        (Animated, 'Animated'),
    )

    genre = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        choices=CHOICES,
        default=None,
    )

    series = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        null=True,
    )

class Episode(models.Model):
    series = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        null=True,
    )

    episodes_watched = models.IntegerField(
        null=True,
        blank=False,
        editable=True,
    )

    title = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    duration = models.IntegerField(
        null=True,
        blank=True,
        editable=True,
    )

    episode_number = models.PositiveIntegerField()

    def __str__(self):
        return self.episode_number

class Season(models.Model):
    series = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        null=True,
    )

    number = models.IntegerField(
        null=False,
        blank=False,
        editable=True,
    )

    episodes = models.ManyToManyField(
        Episode,

    )

class Thread(models.Model):
    title = models.CharField(
        max_length=200
    )

    content = models.TextField()
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
