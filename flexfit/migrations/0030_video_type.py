# Generated by Django 5.0.6 on 2024-11-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexfit', '0029_video_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='Type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
