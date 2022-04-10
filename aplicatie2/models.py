from django.db import models
from aplicatie1.models import Location
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Resorts(models.Model):
    objects = None
    resort_choices = (('Beginner', 'BEGINNER'),
                      ('Intermediate', 'INTERMEDIATE'),
                      ('Expert', 'EXPERT'))

    name = models.CharField(max_length=100)
    resort_type = models.CharField(max_length=20, choices=resort_choices)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resort_type} {self.name}"


class Profile(models.Model):
    skill_choices = (('Beginner', 'BEGINNER'),
                     ('Intermediate', 'INTERMEDIATE'),
                     ('Expert', 'EXPERT'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    assumed_technical_ski_level = models.CharField(max_length=30, choices=skill_choices)
    years_of_experience = models.IntegerField(blank=True)
    money_to_spend = models.IntegerField(blank=True)

    @receiver(post_save, sender=user)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=user)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()





















# class UserExtend(User):
#
#     user_resorts = models.ForeignKey(Resorts, on_delete = models.CASCADE)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name} {self.user_resorts.name}"


