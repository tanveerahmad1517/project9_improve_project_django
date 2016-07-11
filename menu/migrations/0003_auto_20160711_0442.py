# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 09:51
from __future__ import unicode_literals

from django.db import migrations, models


def change_to_date(apps, schema_editor):
    Menu = apps.get_model("menu", "menu")
    for menu in Menu.objects.all():
        menu.expiration_date_new = menu.expiration_date.date()
        menu.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AddField("Menu", "expiration_date_new", models.DateField(blank=True, null=True)),
        migrations.RunPython(change_to_date),
        migrations.RemoveField("Menu", "expiration_date"),
        migrations.RenameField("Menu", "expiration_date_new", "expiration_date")
    ]