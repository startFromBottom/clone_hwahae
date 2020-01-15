# Generated by Django 2.2.4 on 2020-01-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20200111_0800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='bad_review',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='review',
            name='favorites',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='review',
            name='good_review',
            field=models.TextField(default=''),
        ),
    ]
