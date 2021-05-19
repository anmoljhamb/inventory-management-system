# Generated by Django 3.2.3 on 2021-05-19 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_orderrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.PositiveIntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.PositiveIntegerField(default=0)),
                ('group_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.groupname')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.user')),
            ],
        ),
    ]