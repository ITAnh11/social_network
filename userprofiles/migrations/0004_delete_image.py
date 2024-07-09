from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0003_userprofile_address_work_userprofile_place_birth_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
