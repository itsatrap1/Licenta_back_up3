from django.db import models
from aplicatie1.models import Location
from django.contrib.auth.models import User

# Create your models here.


class Logs(models.Model):

    action_choices = (('created', 'created'),
                      ('updated', 'updated'),
                      ('refresh', 'refresh'))

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    action = models.CharField('Action', max_length=10, choices=action_choices)
    url = models.CharField('URL', max_length=100)


class Pontaj(models.Model):

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)


class Companies(models.Model):

    objects = None
    company_choices = (('Beginner', 'BEGINNER'),
                       ('Intermediate', 'INTERMEDIATE'),
                       ('Expert', 'EXPERT'))

    name = models.CharField(max_length = 100)
    website = models.CharField(max_length = 50)
    company_type = models.CharField(max_length = 20, choices = company_choices)
    location = models.ForeignKey(Location, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.company_type} {self.name}"


class UserExtend(User):

    customer = models.ForeignKey(Companies, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.customer.name}"
