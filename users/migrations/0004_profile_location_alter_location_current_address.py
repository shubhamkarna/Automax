# Generated by Django 4.1.5 on 2023-01-17 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_location_state_location_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.location'),
        ),
        migrations.AlterField(
            model_name='location',
            name='current_address',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]