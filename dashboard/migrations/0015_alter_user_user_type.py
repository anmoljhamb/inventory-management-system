# Generated by Django 3.2.3 on 2021-05-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('User', 'User'), ('Group Admin', 'Group Admin')], default='User', max_length=100, null=True),
        ),
    ]
