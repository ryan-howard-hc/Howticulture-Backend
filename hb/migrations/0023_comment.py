# Generated by Django 4.2.4 on 2023-08-28 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hb', '0022_userfavoriteplants_plant_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='hb.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hb.user')),
            ],
        ),
    ]
