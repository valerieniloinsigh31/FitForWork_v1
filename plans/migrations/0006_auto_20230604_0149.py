# Generated by Django 3.2.19 on 2023-06-04 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0005_goal'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Type',
            new_name='PlanType',
        ),
        migrations.RenameField(
            model_name='goal',
            old_name='type',
            new_name='goal',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='type',
            new_name='plantype',
        ),
        migrations.RenameField(
            model_name='plantype',
            old_name='type',
            new_name='plantype',
        ),
        migrations.AlterField(
            model_name='plan',
            name='goal',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.SET_NULL, to='plans.goal'),
        ),
    ]