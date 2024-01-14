# Generated by Django 4.2.7 on 2024-01-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_dailytasksolvers_solvers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailytasksolvers',
            name='solvers',
        ),
        migrations.DeleteModel(
            name='Solver',
        ),
        migrations.AddField(
            model_name='dailytasksolvers',
            name='solvers',
            field=models.ManyToManyField(to='app.profile'),
        ),
    ]
