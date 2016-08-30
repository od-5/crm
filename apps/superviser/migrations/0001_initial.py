# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0015_remove_city_surfaces'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Superviser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.ManyToManyField(to='city.City', null=True, verbose_name='\u0413\u043e\u0440\u043e\u0434\u0430', blank=True)),
                ('superviser', models.OneToOneField(verbose_name='\u0421\u0443\u043f\u0435\u0440\u0432\u0430\u0439\u0437\u0435\u0440', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0441\u0443\u043f\u0435\u0440\u0432\u0430\u0439\u0437\u0435\u0440\u0435',
                'verbose_name_plural': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0441\u0443\u043f\u0435\u0440\u0432\u0430\u0439\u0437\u0435\u0440\u0430\u0445',
            },
            bases=(models.Model,),
        ),
    ]
