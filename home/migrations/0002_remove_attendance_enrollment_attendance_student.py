# Generated by Django 5.0.1 on 2024-05-20 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='enrollment',
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.student'),
        ),
    ]
