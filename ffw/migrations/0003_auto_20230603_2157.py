# Generated by Django 3.2.19 on 2023-06-03 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ffw', '0002_rename_plans_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='sku',
        ),
        migrations.AddField(
            model_name='plan',
            name='goal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('technique', models.TextField()),
                ('occupation', models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.SET_NULL, to='ffw.occupation')),
            ],
        ),
    ]
