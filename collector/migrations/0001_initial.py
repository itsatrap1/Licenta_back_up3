# Generated by Django 3.2.9 on 2022-05-08 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='date happened')),
                ('user_id', models.CharField(max_length=16)),
                ('content_id', models.CharField(max_length=16)),
                ('event', models.CharField(max_length=200)),
                ('session_id', models.CharField(max_length=128)),
            ],
        ),
    ]
