# Generated by Django 4.2.7 on 2023-11-23 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turbosquid', '0002_comment_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductLike',
        ),
    ]
