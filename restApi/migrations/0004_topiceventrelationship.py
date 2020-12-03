# Generated by Django 3.1.2 on 2020-12-03 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restApi', '0003_auto_20201124_0112'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicEventRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restApi.event')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restApi.topic')),
            ],
            options={
                'unique_together': {('topic', 'event')},
            },
        ),
    ]