# Generated by Django 4.0 on 2023-08-25 22:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sindikat_app', '0008_news_title_cyrillic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content_cyrillic',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
