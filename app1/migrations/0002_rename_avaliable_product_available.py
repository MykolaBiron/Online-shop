# Generated by Django 5.2.3 on 2025-06-12 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='avaliable',
            new_name='available',
        ),
    ]
