# Generated by Django 3.2.9 on 2021-11-24 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expenses',
            options={'ordering': ['-date']},
        ),
    ]
