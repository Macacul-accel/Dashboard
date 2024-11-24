# Generated by Django 5.1.2 on 2024-11-19 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_card_frame_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='race',
            new_name='monster_race',
        ),
        migrations.AddField(
            model_name='card',
            name='spell_trap_race',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
