# Generated by Django 4.2.4 on 2023-08-24 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0007_remove_communitypost_image_url_communitypost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='slug',
            field=models.PositiveIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
