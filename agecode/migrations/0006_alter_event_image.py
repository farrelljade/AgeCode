# Generated by Django 4.2.9 on 2024-01-17 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agecode', '0005_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='event_images/'),
        ),
    ]
