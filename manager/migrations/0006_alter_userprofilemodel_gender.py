# Generated by Django 4.2.2 on 2023-06-29 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_rename_avatar_userprofilemodel_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Other'), (2, 'Male'), (3, 'Female')], null=True),
        ),
    ]