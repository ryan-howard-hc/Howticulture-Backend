# Generated by Django 4.2.4 on 2023-08-25 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0010_delete_usernotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfavoriteplants',
            name='plant',
        ),
        migrations.DeleteModel(
            name='Plant',
        ),
    ]