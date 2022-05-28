from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, Avg

import apkstore.storage_backends
from account.models import Account
from apkstore import settings
from developer.models import DevAccount


class AppKind(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class AppCategory(models.Model):
    name = models.CharField(max_length=32)
    kind = models.ForeignKey(AppKind, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AppAgeLimit(models.Model):
    name = models.CharField(max_length=10, unique=True)
    desc = models.CharField(max_length=500)
    min_age = models.SmallIntegerField()

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    desc = models.TextField()
    author = models.ForeignKey(DevAccount, on_delete=models.CASCADE)
    kind = models.ForeignKey(AppKind, on_delete=models.CASCADE)
    category = models.ManyToManyField(AppCategory, blank=True)
    age_limit = models.ForeignKey(AppAgeLimit, on_delete=models.CASCADE)
    download_counter = models.PositiveBigIntegerField(default=0)
    last_update = models.DateField(auto_created=True, auto_now_add=True)
    version = models.CharField(max_length=16, default='0.0.1')
    apkfile = models.FileField()

    @property
    def average_rating(self):
        return self.rating_set.all().aggregate(Avg('rate'))['rate__avg']

    class Meta:
        ordering = ['-download_counter']
        constraints = [
            UniqueConstraint(fields=['name', 'author'], name='createds_once')
        ]

    def __str__(self):
        return self.name


class Comment(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        constraints = [
            UniqueConstraint(fields=['app', 'user'], name='commented_once')
        ]

    def __str__(self):
        return self.comment[:500]


class Rating(models.Model):
    rate = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(rate__range=(1, 5)), name='valid_rate'),
            UniqueConstraint(fields=['user', 'app'], name='rated_once')
        ]

    def __str__(self):
        return f'{self.app.name} {self.user.username} {str(self.rate)}'
