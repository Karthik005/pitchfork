# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pitch.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DevData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('git_url', models.URLField()),
                ('data', models.ForeignKey(to='pitch.Data', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('date', models.DateField()),
                ('pitch', models.TextField()),
                ('document', models.FileField(upload_to=pitch.models.upload_path, blank=True)),
                ('dev_state', models.CharField(max_length=50)),
                ('prog_langs', models.ManyToManyField(to='users.Programming_language')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PitchData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_vol', models.PositiveIntegerField(default=0)),
                ('dev_start_date', models.DateField()),
                ('app_close_date', models.DateField()),
                ('data', models.ForeignKey(to='pitch.Data', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='data',
            name='pitch',
            field=models.ForeignKey(to='pitch.Pitch', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
