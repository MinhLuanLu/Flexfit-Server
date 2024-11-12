# Generated by Django 5.0.6 on 2024-10-04 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flexfit', '0016_rename_pertein_percentage_tracking_calorie_daily_protein_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Calorie_Percentage',
            new_name='Calorie_Did_Take',
        ),
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Carb_Percentage',
            new_name='Carb_Did_Take',
        ),
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Fat_Percentage',
            new_name='Fat_Did_Take',
        ),
        migrations.RenameField(
            model_name='tracking_calorie_daily',
            old_name='Protein_Percentage',
            new_name='Protein_Did_Take',
        ),
    ]
