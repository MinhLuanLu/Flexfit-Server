# Generated by Django 5.0.6 on 2024-09-18 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flexfit', '0009_information_calorie_daily_information_carb_daily_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='information',
            old_name='Calorie_Daily',
            new_name='Average_Calorie',
        ),
    ]
