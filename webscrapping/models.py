from django.db import models


class Resorts(models.Model):

    name = models.CharField(max_length=250)
    lowest_point = models.CharField(max_length=10)
    highest_point = models.CharField(max_length=10)
    difference = models.CharField(max_length=10)
    easy = models.CharField(max_length=10)
    intermediate = models.CharField(max_length=10)
    difficult = models.CharField(max_length=10)
    adult_ticket = models.CharField(max_length=10)
    youth_ticket = models.CharField(max_length=10)
    children_ticket = models.CharField(max_length=10)
    circulating_ropeway_gondola_lift = models.CharField(max_length=10)
    chairlift = models.CharField(max_length=10)
    tbar_lift = models.CharField(max_length=10)
    rope_tow_baby_lift = models.CharField(max_length=10)
    aerial_tramway = models.CharField(max_length=10)
    moving_carpet = models.CharField(max_length=10)
    combined_installation_gondola_chair = models.CharField(max_length=10)
    funicular = models.CharField(max_length=10)
    cog_railway = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    class Admin:
        pass






