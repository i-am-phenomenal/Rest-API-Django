# Generated by Django 3.1.2 on 2020-11-23 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emailId', models.CharField(default='', max_length=30)),
                ('fullName', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eventName', models.CharField(max_length=50, unique=True)),
                ('eventType', models.CharField(max_length=30)),
                ('eventDate', models.DateTimeField(auto_now=True)),
                ('eventDuration', models.CharField(max_length=20)),
                ('eventHost', models.CharField(max_length=30)),
                ('eventLocation', models.CharField(max_length=30)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('topicName', models.CharField(max_length=40, unique=True)),
                ('shortDesc', models.CharField(max_length=40)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEventRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('eventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restApi.event')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTopicRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('topicId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restApi.topic')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('userId', 'topicId')},
            },
        ),
    ]
