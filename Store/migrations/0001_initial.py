# Generated by Django 2.2.1 on 2019-05-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity_name', models.CharField(max_length=32)),
                ('commodity_id', models.CharField(max_length=32)),
                ('commodity_price', models.FloatField()),
                ('commodity_number', models.IntegerField()),
                ('commodity_data', models.DateField()),
                ('commodity_picture', models.ImageField(upload_to='store/img')),
                ('commodity_safe_data', models.IntegerField()),
                ('commodity_address', models.TextField()),
                ('commodity_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=32)),
                ('login_name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=32)),
                ('address', models.TextField()),
                ('logo', models.ImageField(upload_to='store/img')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('parent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='store/img')),
                ('commodity', models.ForeignKey(on_delete=True, to='Store.Commodity')),
            ],
        ),
        migrations.AddField(
            model_name='commodity',
            name='shop',
            field=models.ManyToManyField(to='Store.Store'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='type',
            field=models.ForeignKey(on_delete=True, to='Store.Type'),
        ),
    ]
