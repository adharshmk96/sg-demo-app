# Generated by Django 3.2.7 on 2021-09-06 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='ApprovalRequest',
        ),
    ]
