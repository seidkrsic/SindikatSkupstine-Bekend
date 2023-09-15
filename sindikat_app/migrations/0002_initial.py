# Generated by Django 4.0 on 2023-08-24 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0001_initial'),
        ('sindikat_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.profile'),
        ),
        migrations.AddField(
            model_name='image',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gallery', to='sindikat_app.news'),
        ),
        migrations.AddField(
            model_name='document',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='sindikat_app.session'),
        ),
        migrations.AddField(
            model_name='agenda_item',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agenda_items', to='sindikat_app.session'),
        ),
    ]
