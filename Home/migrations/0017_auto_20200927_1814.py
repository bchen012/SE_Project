# Generated by Django 3.1 on 2020-09-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0016_auto_20200927_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='recommended_price',
            field=models.IntegerField(default=0),
        ),
    ]