# Generated by Django 2.2.5 on 2019-09-24 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Quotes',
            new_name='Quote',
        ),
    ]
