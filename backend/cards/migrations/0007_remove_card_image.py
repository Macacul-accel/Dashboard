# Generated by Django 5.1.2 on 2024-11-15 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_alter_card_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='image',
        ),
    ]
