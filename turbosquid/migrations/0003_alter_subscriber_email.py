# Generated by Django 4.2.6 on 2023-11-02 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbosquid', '0002_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
