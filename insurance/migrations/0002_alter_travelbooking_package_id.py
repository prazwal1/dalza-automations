# Generated by Django 5.2.1 on 2025-06-17 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelbooking',
            name='package_id',
            field=models.CharField(blank=True, choices=[('Everest Region', 'Everest Region'), ('Annapurna Circuit', 'Annapurna Region'), ('Langtang Valley', 'Langtang Valley'), ('Manaslu Circuit', 'Manaslu Circuit')], max_length=50),
        ),
    ]
