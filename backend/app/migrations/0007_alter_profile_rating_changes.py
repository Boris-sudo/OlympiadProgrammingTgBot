# Generated by Django 4.2.7 on 2024-01-12 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_ratingchanges_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rating_changes',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.ratingchanges'),
        ),
    ]
