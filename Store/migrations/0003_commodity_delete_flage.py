# Generated by Django 2.2.1 on 2019-05-21 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_auto_20190520_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='delete_flage',
            field=models.CharField(default='false', max_length=32),
        ),
    ]
