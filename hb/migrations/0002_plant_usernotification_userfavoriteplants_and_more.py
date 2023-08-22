# Generated by Django 4.2.4 on 2023-08-22 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trefle_id', models.PositiveIntegerField(unique=True)),
                ('common_name', models.CharField(blank=True, max_length=100)),
                ('scientific_name', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('family_common_name', models.CharField(max_length=100)),
                ('genus_id', models.PositiveIntegerField()),
                ('observations', models.TextField(blank=True)),
                ('vegetable', models.BooleanField(default=False)),
                ('image_url', models.URLField(blank=True)),
                ('genus', models.CharField(max_length=100)),
                ('family', models.CharField(max_length=100)),
                ('foliage_texture', models.CharField(blank=True, max_length=20)),
                ('foliage_color', models.CharField(blank=True, max_length=20)),
                ('leaf_retention', models.BooleanField(default=False)),
                ('fruit_conspicuous', models.BooleanField(default=False)),
                ('fruit_color', models.CharField(blank=True, max_length=20)),
                ('growth_form', models.CharField(blank=True, max_length=50)),
                ('growth_habit', models.CharField(blank=True, max_length=50)),
                ('growth_rate', models.CharField(blank=True, max_length=50)),
                ('shape_and_orientation', models.CharField(blank=True, max_length=50)),
                ('light', models.PositiveIntegerField(null=True)),
                ('atmospheric_humidity', models.PositiveIntegerField(null=True)),
                ('soil_nutriments', models.PositiveIntegerField(null=True)),
                ('soil_salinity', models.PositiveIntegerField(null=True)),
                ('soil_texture', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFavoritePlants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hb.plant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]