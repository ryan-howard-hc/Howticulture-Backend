# Generated by Django 4.2.4 on 2023-08-25 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0012_communitypost_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitypost',
            name='image',
        ),
        migrations.RemoveField(
            model_name='communitypost',
            name='image_url',
        ),
    ]