# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schematicsapp', '0003_auto_20170218_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(default='no name', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_id', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='schematicmodel',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='schematicmodel',
            name='schematic_tags',
            field=models.ManyToManyField(to='schematicsapp.TagModel'),
        ),
    ]