# Generated by Django 4.2.2 on 2023-06-14 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='authors',
            new_name='author',
        ),
    ]
