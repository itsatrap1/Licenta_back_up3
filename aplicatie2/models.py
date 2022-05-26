from django.db import models
from aplicatie1.models import Location
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from webscrapping.models import Resorts


class Logs(models.Model):
    action_choices = (('created', 'created'),
                      ('updated', 'updated'),
                      ('refresh', 'refresh'))

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    action = models.CharField('Action', max_length=10, choices=action_choices)
    url = models.CharField('URL', max_length=100)


class ResortUserRating(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    resorts = models.ForeignKey(Resorts, on_delete = models.CASCADE)
    resort_rating = models.CharField(max_length = 10)
    rated_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'user_rating'





