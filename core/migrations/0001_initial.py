# Generated by Django 4.2.2 on 2023-06-14 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('name', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False, verbose_name='name')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.PositiveBigIntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('reserve', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('authors', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_author', to='core.author')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
    ]
