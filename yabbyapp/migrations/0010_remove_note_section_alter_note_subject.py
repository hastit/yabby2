# Generated by Django 5.1 on 2024-09-30 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yabbyapp', '0009_alter_note_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='section',
        ),
        migrations.AlterField(
            model_name='note',
            name='subject',
            field=models.CharField(choices=[('Mathématiques', 'Mathématiques'), ('Physique-chimie', 'Physique-chimie'), ('Histoire', 'Histoire'), ('Géographie', 'Géographie'), ('SES', 'SES'), ('Sciences numériques et technologie', 'Sciences numériques et technologie'), ('Français', 'Français'), ('SVT', 'SVT'), ('Anglais', 'Anglais')], max_length=50),
        ),
    ]
