# Generated by Django 4.0.1 on 2022-01-29 16:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelingMechanic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='askPrice',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='commission',
            name='images',
            field=models.ImageField(default='default.png', upload_to='commissionpic/'),
        ),
        migrations.AlterField(
            model_name='commission',
            name='description',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='commission',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]