# Generated by Django 4.2.9 on 2024-01-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agecode', '0004_event_event_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='event_images/'),
        ),
    ]