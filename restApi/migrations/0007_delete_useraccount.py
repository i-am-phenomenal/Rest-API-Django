# Generated by Django 3.1.2 on 2020-12-09 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restApi', '0006_useraccount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAccount',
        ),
    ]