# Generated by Django 4.0 on 2023-09-02 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sindikat_app', '0017_alter_company_options_remove_document_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_address_cyrillic',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_job_cyrillic',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_name_cyrillic',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
