# Generated by Django 5.0.1 on 2024-05-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_face_encoding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='face_encoding',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]