# Generated by Django 3.2.9 on 2022-04-18 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscrapping', '0002_remove_resorts_people_mover'),
    ]

    operations = [
        migrations.AddField(
            model_name='resorts',
            name='rating',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
