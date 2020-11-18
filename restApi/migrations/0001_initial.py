# Generated by Django 3.1.2 on 2020-11-18 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('topicName', models.CharField(max_length=40)),
                ('shortDesc', models.CharField(max_length=40)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emailId', models.CharField(default='', max_length=30)),
                ('fullName', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
