# Generated by Django 4.0 on 2023-08-25 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_profile_secretary'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio_cyrillic',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='name_cyrillic',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
