# Generated by Django 2.2.14 on 2020-07-23 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publisher_id',
            new_name='publisher',
        ),
    ]
