# Generated by Django 5.1.3 on 2025-02-20 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='toppings',
            field=models.ManyToManyField(blank=True, to='menu.topping'),
        ),
    ]
