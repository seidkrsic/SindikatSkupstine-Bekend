# Generated by Django 4.0 on 2023-08-24 09:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda_Item',
            fields=[
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_url', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImportantDocument',
            fields=[
                ('file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('important', models.BooleanField(blank=True, default=False, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('main', models.BooleanField(blank=True, default=False)),
                ('category', models.CharField(choices=[('president', 'President'), ('vice-president', 'Vice-president'), ('board-member', 'Board-Member')], default='president', max_length=100)),
                ('image_url', models.ImageField(blank=True, default='ArtBoard_2.png', null=True, upload_to='')),
                ('content', models.TextField(blank=True, max_length=99999, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
