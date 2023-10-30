# Generated by Django 4.2.6 on 2023-10-28 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turbosquid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pics')),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='parent',
            new_name='category',
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
        migrations.AddField(
            model_name='files',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turbosquid.product'),
        ),
    ]
