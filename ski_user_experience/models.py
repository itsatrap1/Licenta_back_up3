from select2 import fields
import select2
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from webscrapping.models import Resorts
from django.dispatch import receiver


class AdditionalInformationModel(models.Model):
    objects = None
    skill_choices = (('Beginner', 'BEGINNER'),
                     ('Intermediate', 'INTERMEDIATE'),
                     ('Expert', 'EXPERT'))

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    age = models.PositiveIntegerField(blank = True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    assumed_technical_ski_level = models.CharField(max_length = 30, choices = skill_choices)
    years_of_experience = models.PositiveIntegerField(blank = True)
    money_to_spend = models.PositiveIntegerField(blank = True)
    resort_choice = models.ManyToManyField(Resorts, blank = True, null = True, related_name = 'resorts_list')

    def __str__(self):
        return self.user.username

