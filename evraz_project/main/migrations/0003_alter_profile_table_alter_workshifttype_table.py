# Generated by Django 4.2 on 2023-05-04 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_actiontype_authgroup_authgrouppermissions_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='profile',
            table='profile',
        ),
        migrations.AlterModelTable(
            name='workshifttype',
            table='work_shift_type',
        ),
    ]
