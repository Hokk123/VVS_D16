# Generated by Django 4.0.4 on 2022-05-01 22:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0002_post_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]
