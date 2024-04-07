from django.db import migrations, models
import posts.models

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaofposts',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=posts.models.post_directory_path),
        ),
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
