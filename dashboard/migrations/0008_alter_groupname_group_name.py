# Generated by Django 3.2.3 on 2021-05-18 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20210518_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupname',
            name='group_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
