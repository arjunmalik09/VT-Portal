# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('aadhar_card_no', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.CharField(unique=True, max_length=60)),
                ('mobile_no', models.CharField(unique=True, max_length=20)),
                ('gender', models.CharField(max_length=10)),
                ('apt_no', models.CharField(max_length=10)),
                ('locality_name', models.CharField(max_length=80)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('username', models.CharField(unique=True, max_length=30)),
                ('psswd', models.CharField(max_length=30)),
                ('pincode', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'user_profile',
                'managed': False,
            },
        ),
    ]
