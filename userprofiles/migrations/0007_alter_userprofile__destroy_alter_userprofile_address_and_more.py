# Generated by Django 4.2.11 on 2024-05-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0006_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='_destroy',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_work',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='place_birth',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='social_link',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='work',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
