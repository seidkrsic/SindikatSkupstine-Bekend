# Generated by Django 4.0 on 2023-09-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sindikat_app', '0032_alter_news_created_alter_session_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created',
            field=models.DateField(null=True),
        ),
    ]
