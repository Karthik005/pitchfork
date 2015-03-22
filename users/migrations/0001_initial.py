# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('user_ref', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('date_of_birth', models.DateField()),
                ('educational_qualifications', models.CharField(max_length=1000)),
                ('experience', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Programming_language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prog_lang_name', models.CharField(unique=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detail',
            name='prog_langs',
            field=models.ManyToManyField(to='users.Programming_language'),
            preserve_default=True,
        ),
    ]
