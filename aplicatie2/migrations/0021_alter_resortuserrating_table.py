# Generated by Django 3.2.9 on 2022-05-10 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie2', '0020_resortuserrating'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='resortuserrating',
            table='user_rating',
        ),
    ]