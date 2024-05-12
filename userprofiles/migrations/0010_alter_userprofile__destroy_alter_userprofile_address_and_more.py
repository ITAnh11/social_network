# Generated by Django 4.2.11 on 2024-05-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0009_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='_destroy',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_work',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default=' ', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=' ', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='place_birth',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='social_link',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='work',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
    ]
