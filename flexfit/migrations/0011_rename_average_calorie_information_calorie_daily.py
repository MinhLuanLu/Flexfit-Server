# Generated by Django 5.0.6 on 2024-09-18 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flexfit', '0010_rename_calorie_daily_information_average_calorie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='information',
            old_name='Average_Calorie',
            new_name='Calorie_Daily',
        ),
    ]
