# Generated by Django 3.2.10 on 2024-04-10 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Message'},
        ),
    ]