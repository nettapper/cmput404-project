# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 00:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_remove_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='user',
            new_name='requestee',
        ),
        migrations.AlterUniqueTogether(
            name='followingrelationship',
            unique_together=set([('user', 'follows')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set([('requestee', 'requester')]),
        ),
    ]
