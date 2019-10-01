# Generated by Django 2.2 on 2019-09-03 23:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20190903_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('tag', models.CharField(max_length=100, verbose_name='course tag')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course')),
            ],
            options={
                'verbose_name': 'course tag',
                'verbose_name_plural': 'course tag',
            },
        ),
    ]
