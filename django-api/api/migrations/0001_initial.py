# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('song', models.CharField(max_length=100)),
                ('tags', django.contrib.postgres.fields.ArrayField(default=list, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('displayName', models.CharField(max_length=50)),
                ('tagLine', models.CharField(max_length=200, blank=True)),
                ('label', models.CharField(max_length=50, blank=True)),
                ('description', models.TextField(blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(default=list, base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None), size=None)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='track',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
        migrations.AddField(
            model_name='file',
            name='track',
            field=models.ForeignKey(to='api.Track'),
        ),
        migrations.AddField(
            model_name='comment',
            name='track',
            field=models.ForeignKey(to='api.Track'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='track',
            field=models.ForeignKey(to='api.Track'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='remixer',
            field=models.ForeignKey(to='api.User'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='track',
            field=models.ForeignKey(to='api.Track'),
        ),
    ]
