# Generated by Django 3.2.19 on 2023-06-03 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ffw', '0003_auto_20230603_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='technique',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.SET_NULL, to='ffw.technique'),
            preserve_default='True',
        ),
    ]
