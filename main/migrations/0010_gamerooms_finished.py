# Generated by Django 2.2.6 on 2020-01-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20191231_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamerooms',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
