# Generated by Django 5.1.2 on 2024-11-05 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverification',
            old_name='verifaction_token',
            new_name='verification_token',
        ),
    ]