# Generated by Django 4.2.7 on 2023-11-23 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turbosquid', '0003_delete_productlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='user',
        ),
    ]