# Generated by Django 3.2.3 on 2021-10-02 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy_funball', '0003_auto_20210918_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choices',
            old_name='player_has_been_processed',
            new_name='player_point_awarded',
        ),
        migrations.RenameField(
            model_name='choices',
            old_name='team_has_been_processed',
            new_name='team_point_awarded',
        ),
    ]
