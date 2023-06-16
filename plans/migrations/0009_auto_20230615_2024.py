# Generated by Django 3.2.19 on 2023-06-15 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0008_auto_20230615_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tier', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Level',
        ),
        migrations.AddField(
            model_name='plan',
            name='tier',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.SET_NULL, to='plans.tier'),
            preserve_default='True',
        ),
    ]