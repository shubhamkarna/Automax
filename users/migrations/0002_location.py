# Generated by Django 4.1.5 on 2023-01-17 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_address', models.CharField(max_length=128)),
                ('permanent_address', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(max_length=64)),
            ],
        ),
    ]
