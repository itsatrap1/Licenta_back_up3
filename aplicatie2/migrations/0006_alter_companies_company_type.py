# Generated by Django 3.2.9 on 2022-03-26 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie2', '0005_userextend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='company_type',
            field=models.CharField(choices=[('Beginner', 'BEGINNER'), ('Intermediate', 'INTERMEDIATE'), ('Expert', 'EXPERT')], max_length=20),
        ),
    ]