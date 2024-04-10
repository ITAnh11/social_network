# Generated by Django 5.0.2 on 2024-04-05 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversation_id', models.IntegerField(unique=True)),
                ('title', models.TextField(max_length=255)),
            ],
        ),
    ]