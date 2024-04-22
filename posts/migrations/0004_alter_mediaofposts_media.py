# Generated by Django 4.2.11 on 2024-04-22 18:43

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_mediaofposts_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaofposts',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=posts.models.post_directory_path),
        ),
    ]
