# Generated by Django 4.0 on 2023-09-02 11:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sindikat_app', '0014_alter_agenda_item_session_alter_agenda_item_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_name', models.CharField(max_length=1000)),
                ('company_address', models.CharField(max_length=1000)),
                ('company_job', models.CharField(max_length=1000)),
                ('rates', models.IntegerField(default=3, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_documents', to='sindikat_app.company'),
        ),
    ]
