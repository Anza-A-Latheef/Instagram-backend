# Generated by Django 5.1.2 on 2024-10-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagramapp', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]