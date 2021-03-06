# Generated by Django 2.2 on 2019-08-27 17:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('mobile', models.CharField(max_length=12, verbose_name='phone number')),
                ('course_name', models.CharField(max_length=50, verbose_name='course name')),
            ],
            options={
                'verbose_name': "user's questions",
                'verbose_name_plural': "user's questions",
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('message', models.CharField(max_length=200, verbose_name='content')),
                ('has_read', models.BooleanField(default=False, verbose_name='has read or not')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': "user's message",
                'verbose_name_plural': "user's message",
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('fav_id', models.IntegerField(verbose_name='favorite id')),
                ('fav_type', models.IntegerField(choices=[(1, 'course'), (2, 'organization'), (3, 'teacher')], default=1, verbose_name='type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': "user's favorite",
                'verbose_name_plural': "user's favorite",
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': "user's course",
                'verbose_name_plural': "user's course",
            },
        ),
        migrations.CreateModel(
            name='CourseComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('comments', models.CharField(max_length=200, verbose_name='content')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'course comments',
                'verbose_name_plural': 'course comments',
            },
        ),
    ]
