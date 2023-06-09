# Generated by Django 3.2.19 on 2023-06-06 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plans', '0005_auto_20230606_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=300)),
                ('phone_number', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=40)),
                ('eircode', models.CharField(blank=True, max_length=15, null=True)),
                ('town_or_city', models.CharField(max_length=25)),
                ('street_address_1', models.CharField(max_length=100)),
                ('street_address_2', models.CharField(blank=True, max_length=100, null=True)),
                ('county', models.CharField(blank=True, max_length=60, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('lineitem_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.orderplan')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plans.plan')),
            ],
        ),
    ]
