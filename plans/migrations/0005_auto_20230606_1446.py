# Generated by Django 3.2.19 on 2023-06-06 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_plan_has_levels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='has_levels',
        ),
        migrations.RemoveField(
            model_name='type',
            name='type',
        ),
    ]