# Generated by Django 5.1.1 on 2024-09-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexfit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
