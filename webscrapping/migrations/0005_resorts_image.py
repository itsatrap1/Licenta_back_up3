# Generated by Django 3.2.9 on 2022-05-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscrapping', '0004_auto_20220516_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='resorts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
