# Generated by Django 5.2.1 on 2025-06-19 08:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_rename_pp_number_client_passport_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('ward_no', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='city',
        ),
        migrations.RemoveField(
            model_name='client',
            name='province',
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_client', to='clients.address'),
        ),
        migrations.AlterField(
            model_name='client',
            name='perma_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permanent_client', to='clients.address'),
        ),
    ]
