# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 13:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construct', '0012_auto_20170314_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='construct',
            name='deletions',
        ),
        migrations.RemoveField(
            model_name='construct',
            name='insertions',
        ),
        migrations.RemoveField(
            model_name='construct',
            name='modifications',
        ),
        migrations.RemoveField(
            model_name='construct',
            name='mutations',
        ),
        migrations.AddField(
            model_name='constructdeletion',
            name='construct',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='construct.Construct'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='constructinsertion',
            name='construct',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='construct.Construct'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='constructmodification',
            name='construct',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='construct.Construct'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='constructmutation',
            name='construct',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='construct.Construct'),
            preserve_default=False,
        ),
    ]