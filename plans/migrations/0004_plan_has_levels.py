# Generated by Django 3.2.19 on 2023-06-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='has_levels',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]