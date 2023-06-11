# Generated by Django 3.2.19 on 2023-06-11 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_auto_20230611_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='technique',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='technique',
            name='image_url',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]