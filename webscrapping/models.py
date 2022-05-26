from django.db import models


class Resorts(models.Model):

    objects = None
    name = models.CharField(max_length=250)
    rating = models.FloatField()
    lowest_point = models.CharField(max_length=10)
    highest_point = models.CharField(max_length=10)
    difference = models.CharField(max_length=10)
    easy = models.CharField(max_length=10)
    intermediate = models.CharField(max_length=10)
    difficult = models.CharField(max_length=10)
    adult_ticket = models.CharField(max_length=10)
    youth_ticket = models.CharField(max_length=10)
    children_ticket = models.CharField(max_length=10)
    resort_lift_number = models.IntegerField()
    img = models.ImageField(upload_to = 'media/images/', blank = True, null = True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']

    class Admin:
        pass






