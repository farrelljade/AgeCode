# Generated by Django 4.2.9 on 2024-02-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agecode', '0010_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='agecode.profile'),
        ),
    ]
