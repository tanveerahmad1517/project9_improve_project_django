# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 09:51
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


def change_to_date(apps, schema_editor):
    Item = apps.get_model("menu", "item")
    for item in Item.objects.all():
        item.created_date_new = item.created_date.date()
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20160711_0442'),
    ]

    operations = [
        migrations.AddField("Item", "created_date_new", models.DateField(
            default=timezone.now)),
        migrations.RunPython(change_to_date),
        migrations.RemoveField("Item", "created_date"),
        migrations.RenameField("Item", "created_date_new", "created_date")
    ]
