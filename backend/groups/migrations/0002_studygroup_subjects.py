# Generated by Django 4.1.2 on 2023-01-27 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroup',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='subjects.subject'),
        ),
    ]
