# Generated by Django 4.2.7 on 2024-01-10 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_olympiad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True, verbose_name='topic name')),
                ('link', models.CharField(max_length=1000, unique=True, verbose_name='topic link')),
            ],
        ),
        migrations.CreateModel(
            name='TopicArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True, verbose_name='topic archive name')),
                ('children', models.ManyToManyField(to='app.topic', verbose_name='topic archive children')),
            ],
        ),
    ]