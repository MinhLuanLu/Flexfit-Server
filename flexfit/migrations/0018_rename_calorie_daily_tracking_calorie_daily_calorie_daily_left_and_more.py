# Generated by Django 5.0.6 on 2024-10-04 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flexfit', '0017_rename_calorie_percentage_tracking_calorie_daily_calorie_did_take_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Calorie_Daily',
            new_name='Calorie_Daily_Left',
        ),
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Carb_Daily',
            new_name='Carb_Daily_Left',
        ),
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Fat_Daily',
            new_name='Fat_Daily_Left',
        ),
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Protein_Daily',
            new_name='Protein_Daily_Left',
        ),
    ]
