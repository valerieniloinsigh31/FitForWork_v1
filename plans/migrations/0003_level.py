# Generated by Django 3.2.19 on 2023-06-04 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_auto_20230604_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('level', models.TextField()),
            ],
        ),
    ]