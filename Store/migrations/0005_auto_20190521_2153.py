# Generated by Django 2.2.1 on 2019-05-21 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_type_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='picture',
            field=models.ImageField(default='store/images/222222.jpg', upload_to='store/images'),
        ),
    ]
