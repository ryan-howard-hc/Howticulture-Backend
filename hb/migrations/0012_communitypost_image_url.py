# Generated by Django 4.2.4 on 2023-08-25 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0011_remove_userfavoriteplants_plant_delete_plant'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitypost',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
