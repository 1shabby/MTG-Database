# Generated by Django 4.1.2 on 2022-10-30 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CardRepository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
