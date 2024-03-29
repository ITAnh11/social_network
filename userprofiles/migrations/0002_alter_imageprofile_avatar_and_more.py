import userprofiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='media/users/default/avatar_default.png', upload_to=userprofiles.models.media_directory_path),
        ),
        migrations.AlterField(
            model_name='imageprofile',
            name='background',
            field=models.ImageField(blank=True, default='media/users/default/background_default.jpg', upload_to=userprofiles.models.media_directory_path),
        ),
    ]
