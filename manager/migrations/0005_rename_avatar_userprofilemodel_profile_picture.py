# Generated by Django 4.2.2 on 2023-06-29 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_userprofilemodel_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofilemodel',
            old_name='avatar',
            new_name='profile_picture',
        ),
    ]
