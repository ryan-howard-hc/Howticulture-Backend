# Generated by Django 4.2.4 on 2023-08-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0018_userfavoriteplants_plant_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfavoriteplants',
            name='plant_id',
        ),
        migrations.AddField(
            model_name='userfavoriteplants',
            name='plant_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
