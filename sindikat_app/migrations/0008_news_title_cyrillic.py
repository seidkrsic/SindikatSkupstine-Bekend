# Generated by Django 4.0 on 2023-08-25 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sindikat_app', '0007_agenda_item_title_cyrillic_document_title_cyrillic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='title_cyrillic',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
