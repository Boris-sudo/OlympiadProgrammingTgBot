# Generated by Django 4.2.7 on 2024-02-22 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_dailytaskchecking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestId', models.IntegerField()),
                ('index', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Not Started'), (1, 'Searching For Opponent'), (2, 'In Progress'), (11, 'Winner1'), (12, 'Winner2'), (10, 'Draw')], default=1)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.task')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user1', to='app.profile')),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user2', to='app.profile')),
            ],
        ),
    ]