# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=140)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_backend.Author')),
            ],
        ),
        migrations.CreateModel(
            name='FollowingRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follows', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to='rest_backend.Author')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_backend.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('content', models.CharField(max_length=140)),
                ('description', models.CharField(max_length=140)),
                ('contentType', models.CharField(max_length=32)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_backend.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='rest_backend.Post'),
        ),
    ]
