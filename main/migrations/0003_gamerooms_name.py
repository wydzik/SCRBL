# Generated by Django 2.2.6 on 2019-12-16 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191216_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamerooms',
            name='name',
            field=models.CharField(default='Too lazy to name', max_length=250),
        ),
    ]
