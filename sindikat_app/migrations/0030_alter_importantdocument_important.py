# Generated by Django 4.0 on 2023-09-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sindikat_app', '0029_remove_news_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importantdocument',
            name='important',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
