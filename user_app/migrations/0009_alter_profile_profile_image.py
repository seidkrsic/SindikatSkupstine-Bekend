# Generated by Django 4.0 on 2023-09-13 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_alter_profile_bio_alter_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='http://apisindikat.skupstina.me/images//ArtBoard_2.png', null=True, upload_to=''),
        ),
    ]
