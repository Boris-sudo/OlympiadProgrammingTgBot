# Generated by Django 4.2.7 on 2024-01-13 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_solver_dailytasksolvers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailytasksolvers',
            name='solvers',
        ),
        migrations.AddField(
            model_name='dailytasksolvers',
            name='solvers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.solver'),
        ),
    ]
